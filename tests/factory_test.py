import diay


def test_factory():
    class A: pass
    class B(A): pass
    class C:
        def __init__(self, a: A):
            self.a = a
    i = diay.Injector()
    i.factories[A] = lambda: B()
    c = i.get(C)
    assert isinstance(c.a, B)
    assert isinstance(c.a, A)
