# -*- coding: utf-8 -*-


class Actions(object):
    """
      This class is responsible for registering functions decorated with
      `@action` and accessing them.
    """

    # This is a dict having keys as functions names and values as functions.
    # `register_action` method handles adding functions here.
    registered_actions = {}

    def __getattr__(self, key):
        """
            This is just a proxy to make all the actions from
            `registered_actions` accessible from this instance.

            Example::
                >>> @action
                >>> def my_action():
                >>>     print 'My action has been called.'
                >>> actions = Actions()
                >>> actions.my_action()
                My action has been called.
        """
        try:
            return self.registered_actions[key]
        except KeyError:
            # conforming with __getattr__ spec, as it's an attribute access.
            raise AttributeError(key)

    @classmethod
    def register_action(cls, action_name, action_fn):
        """
            Registers a function to `registered_actions`.
        """
        cls.registered_actions[action_name] = action_fn


def action(func):
    """
        It's a decorator that should be used to create actions.
        Every action that uses it will be available at `FunctTestCase`,
        via `actions` attribute.
    """
    Actions.register_action(func.__name__, func)

    def execute(*args, **kwargs):
        return func(*args, **kwargs)
    return execute
