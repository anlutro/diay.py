import diay


def test_inject_into_function():
    class A: pass
    def f(a: A): return a
    a = diay.Injector().get(f)
    assert isinstance(a, A)


def test_inject_into_constructor():
    class A: pass
    class B:
        def __init__(self, a: A):
            self.a = a
    b = diay.Injector().get(B)
    assert isinstance(b, B)
    assert isinstance(b.a, A)


def test_nested_inject():
    class A: pass
    class B:
        def __init__(self, a: A):
            self.a = a
    class C:
        def __init__(self, b: B):
            self.b = b
    c = diay.Injector().get(C)
    assert isinstance(c, C)
    assert isinstance(c.b, B)
    assert isinstance(c.b.a, A)


def test_inject_decorator_class_property():
    class A: pass
    @diay.inject('a', A)
    class B: pass
    b = diay.Injector().get(B)
    assert isinstance(b.a, A)
