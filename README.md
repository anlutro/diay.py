# Diay - a dependency injection library

[![Build Status](https://travis-ci.org/anlutro/diay.py.svg?branch=master)](https://travis-ci.org/anlutro/diay.py)
[![Latest version on PyPI](https://img.shields.io/pypi/v/diay.svg?maxAge=2592000)](https://pypi.org/project/diay)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Diay is a [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)/[inversion of control](https://en.wikipedia.org/wiki/Inversion_of_control) library for Python 3.5 and higher. It leverages the type hints introduced in 3.5 to allow you to easily call functions or construct classes that require specific types of objects to function.

As an extremely basic and somewhat contrived example - the value of the library doesn't really come into play until you have fairly deeply nested dependencies - let's say you want to render a jinja2 template using some data from an API.

```python
injector = diay.Injector()
injector.set_instance(SomeConfigClass, my_config_object)

@injector.provider
def make_jinja_environment() -> jinja2.Environment:
    return jinja2.Environment()

@injector.provider
def make_api_client(config: SomeConfigClass) -> some.APIclient:
    return some.APIclient(config.api_token)

def render(j2env: jinja2.Environment, apiclient: some.APIclient):
    data = apiclient.get('/some/data')
    template = j2env.get_template('some-template.html.j2', data=data)
    return template.render()

html = injector.call(render)
```
