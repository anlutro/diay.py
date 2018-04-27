import diay


def test_plugin():
    class TestPlugin(diay.Plugin):
        @diay.provider
        def f(self) -> str:
            return 'foo'
    i = diay.Injector()
    i.register_plugin(TestPlugin())
    assert 'foo' == i.get(str)
