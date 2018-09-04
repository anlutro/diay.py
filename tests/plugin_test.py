import diay


def test_plugin():
    class TestPlugin(diay.Plugin):
        @diay.provider
        def f(self) -> str:
            return 'foo'

    i = diay.Injector()
    i.register_plugin(TestPlugin())
    assert 'foo' == i.get(str)


def test_plugin_lazy():
    """
    TestPlugin has a dependency which needs a provider, but whether we
    register the plugin or provider first should not matter. The plugin should
    be lazily instantiated.
    """
    class Dep:
        def __init__(self, v):
            self.v = v

        def f(self):
            return self.v

    class TestPlugin(diay.Plugin):
        def __init__(self, dep: Dep):
            self.dep = dep

        @diay.provider
        def f(self) -> str:
            return self.dep.f()

    i = diay.Injector()
    i.register_plugin(TestPlugin)
    @i.provider
    def provide_dep() -> Dep:
        return Dep('foo')
    assert 'foo' == i.get(str)
