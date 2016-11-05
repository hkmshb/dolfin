"""
Defines unit tests for dolfin.
"""
import os
import sys
import unittest

import dolfin


class FakeCommand(dolfin.Command):
    
    prog = 'fake'
    desc = 'This is a fake implementation of the Command class'

    def __init__(self):
        self.p = None
        self.register = set()

    def _execute(self, args):
        self.register.add('_execute')
        return super(FakeCommand, self)._execute(args)
        
    def _create_parser(self):
        if self.p == None:
            from argparse import ArgumentParser
            
            p = ArgumentParser(prog=self.prog, description=self.desc)
            add = lambda *a, **k: p.add_argument(*a, **k)
            add('-p', '--port', type=int, default=None, help='server port')
            add('--host', help='server hostname')
            add('-s', '--show', action='store_true', help='show server details')
            self.register.add('_create_parser')
            self.p = p
        return self.p
    
    def _handle(self, args):
        self.register.add('_handle')
        if args.show:
            return "server='%s:%s'" % (args.port or 80, args.host or 'localhost')


class CommandTest(unittest.TestCase):
    
    def test_cannot_create_abstract_command(self):
        self.assertRaises(TypeError, dolfin.Command)

    def test_cannot_create_abstract_subcommand(self):
        self.assertRaises(TypeError, dolfin.SubCommand)

    def test_are_best_invoked_using_run_from_argv(self):
        cmd = FakeCommand()
        self.assertEqual(0, len(cmd.register))
        cmd.run_from_argv(['-p', '8080', '-s'])

        self.assertEqual(3, len(cmd.register))
        self.assertTrue(
            '_execute' in cmd.register and
            '_create_parser' in cmd.register and
            '_handle' in cmd.register
        )


if __name__ == '__main__':
    unittest.main()
