import pytest

import diay


def test_call_with_argument_defaults():
    def f(v='foobar'): return v
    i = diay.Injector()
    assert i.call(f) == 'foobar'


def test_raises_exception_when_args_unknown():
    def f(v): return v
    i = diay.Injector()
    with pytest.raises(diay.DiayException):
        i.call(f)


def test_call_injects_dependencies():
    class A: pass
    def f(a: A): return a
    ret = diay.Injector().call(f)
    assert isinstance(ret, A)
