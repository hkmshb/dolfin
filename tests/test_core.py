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


class StorageTest(unittest.TestCase):

    def test_storage_is_instance_of_dict(self):
        s = dolfin.Storage()
        self.assertIsInstance(s, dict)

    def test_can_access_element_using_dot_notation(self):
        foo = dolfin.Storage()
        foo['bar'] = 'baz-qux-norf'
        self.assertEqual('baz-qux-norf', foo.bar)

    def test_can_set_element_using_dot_notation(self):
        foo = dolfin.Storage()
        foo.bar = 'baz-qux-norf'
        self.assertEqual('baz-qux-norf', foo['bar'])

    def test_access_using_unknown_member_returns_None(self):
        foo = dolfin.Storage()
        self.assertIsNone(foo.bar)

    def test_access_using_missing_key_returns_None(self):
        foo = dolfin.Storage()
        self.assertIsNone(foo['bar'])

    def test_can_be_pickled_and_unpickled(self):
        import pickle

        foo = dolfin.Storage(bar='baz')
        out = pickle.dumps(foo)
        self.assertIsNotNone(out)
        
        qux = pickle.loads(out)
        self.assertEqual('baz', qux.bar)

    def test_has_friendly_string_representation(self):
        foo = dolfin.Storage(bar='baz')
        self.assertTrue(repr(foo).startswith('<Storage'))
    
    def test_make_not_given_dict_or_sequence_throws(self):
        self.assertRaises(ValueError, dolfin.Storage.make, 'foo')

    def test_can_make_storage_from_dict(self):
        obj = dolfin.Storage.make(dict(foo='bar'))
        self.assertIsInstance(obj, dolfin.Storage)
        self.assertEqual('bar', obj.foo)

    def test_can_make_storage_from_nested_dicts(self):
        obj = dolfin.Storage.make(dict(
            baz = dict(
                quux = 'norf',
                meta = dict(
                    name = 'simple.conf',
                    path = r'c:\path\to\conf',
                )
            )
        ))
        self.assertIsInstance(obj, dolfin.Storage)
        self.assertIsInstance(obj.baz, dolfin.Storage)
        self.assertIsInstance(obj.baz.meta, dolfin.Storage)


if __name__ == '__main__':
    unittest.main()
