import diay


def test_provider():
    class A:
        def __init__(self, name):
            self.name = name
    @diay.provider
    def f() -> A:
        return A('foo')
    i = diay.Injector()
    i.register_provider(f)
    a = i.get(A)
    assert isinstance(a, A)
    assert 'foo' == a.name


def test_provider_singleton():
    class_count = 0
    class A:
        def __init__(self):
            nonlocal class_count
            class_count += 1
    @diay.provider(singleton=True)
    def f() -> A:
        return A()
    i = diay.Injector()
    i.register_provider(f)
    a1 = i.get(A)
    a2 = i.get(A)
    assert isinstance(a1, A)
    assert a1 is a2


def test_provider_dependencies():
    class A:
        def __init__(self, name):
            self.name = name
    class B:
        def __init__(self, a: A, name):
            self.a = a
            self.name = name
    @diay.provider
    def a() -> A:
        return A('a')
    @diay.provider
    def b(a: A) -> B:
        return B(a, 'b')
    i = diay.Injector()
    i.register_provider(a)
    i.register_provider(b)
    b = i.get(B)
    assert isinstance(b, B)
    assert 'b' == b.name
    assert isinstance(b.a, A)
    assert 'a' == b.a.name


def test_injector_provider_decorator():
    class A:
        def __init__(self, name):
            self.name = name
    i = diay.Injector()

    @i.provider
    def f1() -> A:
        return A('foo')
    a = i.get(A)
    assert isinstance(a, A)
    assert 'foo' == a.name

    @i.provider(singleton=True)
    def f2() -> A:
        return A('foo')
    a = i.get(A)
    assert isinstance(a, A)
    assert 'foo' == a.name
