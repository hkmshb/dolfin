# -*- coding: utf-8 -*-
"""
Defines core functions and classes.
"""

import os
import sys
from abc import ABCMeta, abstractmethod


__all__ = ['CommandError', 'Command', 'SubCommand', 'Storage']



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


class CommandError(Exception):
    """The exception thrown for a command related error."""
    pass


class CommandBase(object, metaclass=ABCMeta):
    """
    Defines the core interfaces for a Command object.
    """

    def __init__(self):
        self.__parser = None

    @abstractmethod
    def _create_parser(self):
        """
        Creates and returns an `ArgumentParser` instance which can be used to
        parse the arguments passed to this command.
        """
        pass
    
    @abstractmethod
    def _handle(self, args):
        """
        Performs the actual operation of the command.
        """
        pass
    
    def _execute(self, args):
        """
        Tries to execute a command; if it raises a CommandError, intercept
        and print it sensibly to stderr
        """
        try:
            output = self._handle(args)
            if output:
                print(output)
        except CommandError as ex:
            sys.stderr.write("Error: %s\n\n:" % str(ex))
            sys.exit(1)
    
    def get_parser(self, force=False):
        """
        Maintains and returns an `ArgumentParser` instance gotten from a call to
        `_create_parse`. A new instance should always be created and returned if
        force is True.
        """
        if not self.__parser or force:
            self.__parser = self._create_parser()
        return self.__parser


class Command(CommandBase):
    """
    Represents the base class for a stand-alone command which is
    capable of having SubCommands.
    """

    def __init__(self):
        super(Command, self).__init__()
        self.__subparsers_builder = None
    
    def get_parser(self, force=False):
        parser = super(Command, self).get_parser(force)
        
        # create subcommands
        if hasattr(self, 'subcommands'):
            self._subcommands = getattr(self, '_subcommands', dict())
            if not self._subcommands:
                builder = self._create_subparsers_builder(parser)

                for _class in self.subcommands:
                    subcommand = _class(builder)
                    self._subcommands[subcommand.name] = subcommand
        
        # return create parser
        return parser

    def run_from_argv(self, argv=None):
        """
        Entry point for running the command.
        """
        argv = (sys.argv[1:] if argv is None else argv)
        parser = self.get_parser()
        args = parser.parse_args(argv)
        self._execute(args)

    def _create_subparsers_builder(self, parser):
        """
        Returns an `ArgumentParser` factory-like object used for creation of
        sub parsers. 
        
        Override in derived classes to change `title`, `description`, `prog` 
        and more for the action object to be created. 
        """
        return parser.add_subparsers(
            title='subcommands', description='valid subommands' 
        )


class SubCommand(CommandBase):
    """
    Represents the base class for a SubCommand object.
    """

    def __init__(self, parser_builder):
        super(SubCommand, self).__init__()
        self._parser_builder = parser_builder
        self._create_parser()
    
    def __call__(self, args):
        self._handle(args)

