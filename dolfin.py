# -*- coding: utf-8 -*-
"""
A collection of general purpose utility functions and classes that can be used
within scripts and web applications.

Copyright (c) 2014, Hazeltek Solutions.
"""

__author__  = 'Hazeltek Solutions'
__version__ = '0.1'


import os
import sys
from abc import ABCMeta, abstractmethod



class CommandError(Exception):
    """The exception thrown for a command related error."""
    pass


class Command(object, metaclass=ABCMeta):
    """Represents the base class for Command objects."""

    def _execute(self, args):
        """
        Tries to execute this command; if it raises a CommandError, intercept it
        and print it sensibly to stderr.
        """
        try:
            output = self._handle(args)
            if output: print(output)
        except CommandError as ex:
            sys.stderr.write("Error: %s\n\n:" % str(ex))
            sys.exit(1)
    
    def print_help(self, prog):
        """
        Prints the help message for this command.
        """
        p = self.create_parser(prog)
        p.print_help()
    
    def run_from_argv(self, argv=None):
        """
        Handles default options then run this command.
        """
        argv = (sys.argv[1:] if argv is None else argv)
        p = self._create_parser()
        args = p.parse_args(argv)

        self._handle_default_args(args)
        self._execute(args)
    
    def _handle_default_args(self, args):
        if hasattr(args, 'pythonpath'):
            sys.path.insert(0, args.pythonpath)
    

    @abstractmethod
    def _create_parser(self):
        """
        Creates and returns the ArgumentParser which will be used to parse the 
        arguments passed to this command. Must be overridden by subclasses.
        """
        pass
    
    @abstractmethod
    def _handle(self, args):
        """
        Performs the actual operation of the command. Must be overridden by 
        subclasses.
        """
        pass


class SubCommand(object, metaclass=ABCMeta):
    """Represents the base class for a SubCommand object."""

    def __init__(self, parent):
        self._subparser = parent.create_subparser(self)
        self._parent = parent
    
    def _error(self, message):
        self._subparser.error(message)

    @abstractmethod
    def __call__(self, args):
        pass


class Storage(dict):
    """
    Represents a dictionary object whose elements can be accessed and set using 
    the dot object notation. Thus in addition to `foo['bar']`, `foo.bar` can 
    equally be used.
    """
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, key):
        return self.__getitem__(key)
    
    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, key):
        return dict.get(self, key, None)
    
    def __getstate__(self):
        return dict(self)

    def __setstate__(self, value):
        dict.__init__(self, value)

    def __repr__(self):
        return '<Storage %s>' % dict.__repr__(self)
    
    @staticmethod
    def make(obj):
        """
        Converts all dict-like elements of a dict or storage object into
        storage objects.
        """
        if not isinstance(obj, (dict,)):
            raise ValueError('obj must be a dict or dict-like object')
        
        _make = lambda d: Storage({ k: d[k] 
            if not isinstance(d[k], (dict, Storage))
            else _make(d[k])
                for k in d.keys()
        })
        return _make(obj)

