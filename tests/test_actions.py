import unittest

from pyfunct.actions import Actions, action

class ActionsTestCase(unittest.TestCase):

    def test_actions_decorator(self):
        actions = Actions()

        @action
        def my_action():
            return 'MyAction'

        self.assertEqual(actions.my_action(), 'MyAction')

    def test_undefined_action_raises_AttributeError(self):
        with self.assertRaises(AttributeError):
            actions = Actions()
            actions.undefined_action()