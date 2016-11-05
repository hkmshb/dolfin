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
