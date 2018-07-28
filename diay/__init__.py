import inspect
import typing


class DiayException(Exception):
    pass


def _wrap_provider_func(func, di_props):
    hints = typing.get_type_hints(func)
    di_props['provides'] = hints['return']

    if not hasattr(func, '__di__'):
        func.__di__ = {}
    func.__di__.update(di_props)

    return func


def provider(func=None, *, singleton=False, injector=None):
    """
    Decorator to mark a function as a provider.

    Args:
        singleton (bool): The returned value should be a singleton or shared
            instance. If False (the default) the provider function will be
            invoked again for every time it's needed for injection.
        injector (Injector): If provided, the function is immediately
            registered as a provider with the injector instance.

    Example:
        @diay.provider(singleton=True)
        def myfunc() -> MyClass:
            return MyClass(args)
    """
    def decorator(func):
        wrapped = _wrap_provider_func(func, {'singleton': singleton})
        if injector:
            injector.register_provider(wrapped)
        return wrapped

    if func:
        return decorator(func)
    return decorator


def _inject_object(obj, var_name, var_type):
    if not hasattr(obj, '__di__'):
        obj.__di__ = {}
    obj.__di__.setdefault('inject', {})[var_name] = var_type
    return obj


def inject(*args, **kwargs):
    """
    Mark a class or function for injection, meaning that a DI container knows
    that it should inject dependencies into it.

    Normally you won't need this as the injector will inject the required
    arguments anyway, but it can be used to inject properties into a class
    without having to specify it in the constructor, or to inject arguments
    that aren't properly type hinted.

    Example:
        @diay.inject('foo', MyClass)
        class MyOtherClass: pass
        assert isinstance(injector.get(MyOtherClass).foo, MyClass)
    """
    def wrapper(obj):
        if inspect.isclass(obj) or callable(obj):
            _inject_object(obj, *args, **kwargs)
            return obj
        raise DiayException("Don't know how to inject into %r" % obj)
    return wrapper


class Plugin:  # pylint: disable=too-few-public-methods
    """
    A plugin is a collection of providers.
    """
    pass


class Injector:
    """
    Class that knows how to do dependency injection.
    """
    def __init__(self):
        self.instances = {}
        self.factories = {}

    def register_plugin(self, plugin: Plugin):
        """
        Register a plugin.
        """
        if inspect.isclass(plugin):
            plugin = self.get(plugin)

        if not isinstance(plugin, Plugin):
            msg = 'plugin %r must be an object of type Plugin' % plugin
            raise DiayException(msg)

        methods = inspect.getmembers(plugin, predicate=inspect.ismethod)
        for _, method in methods:
            if getattr(method, '__di__', {}).get('provides'):
                self.register_provider(method)

    def register_provider(self, func):
        """
        Register a provider function.
        """
        if 'provides' not in getattr(func, '__di__', {}):
            raise DiayException('Function %r is not a provider' % func)
        self.factories[func.__di__['provides']] = func

    def set_factory(self, thing: type, value, overwrite=False):
        """
        Set the factory for something.
        """
        if thing in self.factories and not overwrite:
            raise DiayException('factory for %r already exists' % thing)
        self.factories[thing] = value

    def set_instance(self, thing: type, value, overwrite=False):
        """
        Set an instance of a thing.
        """
        if thing in self.instances and not overwrite:
            raise DiayException('instance for %r already exists' % thing)
        self.instances[thing] = value

    def get(self, thing: type):
        """
        Get an instance of some type.
        """
        if thing in self.instances:
            return self.instances[thing]

        if thing in self.factories:
            fact = self.factories[thing]
            ret = self.get(fact)
            if hasattr(fact, '__di__') and fact.__di__['singleton']:
                self.instances[thing] = ret
            return ret

        if inspect.isclass(thing):
            return self._call_class_init(thing)
        elif callable(thing):
            return self.call(thing)

        raise DiayException('cannot resolve: %r' % thing)

    def call(self, func, *args, **kwargs):
        """
        Call a function, resolving any type-hinted arguments.
        """
        guessed_kwargs = self._guess_kwargs(func)
        for key, val in guessed_kwargs.items():
            kwargs.setdefault(key, val)
        return func(*args, **kwargs)

    def _call_class_init(self, cls):
        # if this statement is true, the class or its parent class(es) does not
        # have an __init__ method defined and as such should not need any
        # constructor arguments to be instantiated.
        if cls.__init__ is object.__init__:
            obj = cls()
        else:
            obj = cls(**self._guess_kwargs(cls.__init__))

        # extra properties defined with @diay.inject
        if 'inject' in getattr(obj, '__di__', {}):
            for prop_name, prop_type in obj.__di__['inject'].items():
                setattr(obj, prop_name, self.get(prop_type))

        return obj

    def _guess_kwargs(self, func):
        kwargs = {}
        hints = typing.get_type_hints(func)
        for arg in hints:
            if arg == 'return':
                continue
            kwargs[arg] = self.get(hints[arg])
        return kwargs

    def provider(self, *args, **kwargs):
        """
        Convenience decorator, shortcut for @diay.provider(injector=self)
        """
        kwargs['injector'] = self
        return provider(*args, **kwargs)
