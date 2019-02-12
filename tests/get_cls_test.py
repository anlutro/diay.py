import pytest

import diay


def test_can_get_class_with_init_defaults():
    class A:
        def __init__(self, v='foobar'):
            self.v = v
    i = diay.Injector()
    a = i.get(A)
    assert isinstance(a, A)
    assert a.v == 'foobar'


def test_raises_exception_when_init_args_unknown():
    class A:
        def __init__(self, v):
            self.v = v
    i = diay.Injector()
    with pytest.raises(diay.DiayException):
        i.get(A)
