import diay


def test_call_injects_dependencies():
    class A: pass
    def f(a: A): return a
    ret = diay.Injector().call(f)
    assert isinstance(ret, A)
