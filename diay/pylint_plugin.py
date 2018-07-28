import astroid


def register(linter):
    pass


def _iter_cls_decorators(cls):
    if cls.decorators:
        yield from cls.decorators.nodes
    for ancestor in cls.ancestors():
        if ancestor.decorators:
            yield from ancestor.decorators.nodes


def transform(cls):
    for node in _iter_cls_decorators(cls):
        if isinstance(node, astroid.Call):
            func = node.func
        else:
            func = node

        if not func.as_string() == 'diay.inject':
            continue

        cls.instance_attrs[node.args[0].value] = [
            inferred.instantiate_class() for inferred in node.args[1].infer()
        ]


astroid.MANAGER.register_transform(astroid.nodes.ClassDef, transform)
