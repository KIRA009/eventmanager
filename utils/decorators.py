import jsonschema
from collections import ChainMap

from .exceptions import AccessDenied


def decorator(func, test_func):
    def inner(*args, **kwargs):
        request = args[0]
        if 'User' in request.__dict__:
            if test_func(request.User):
                return func(*args, **kwargs)
        elif request.user.is_authenticated:
            if test_func(request.user):
                return func(*args, **kwargs)
        raise AccessDenied()

    return inner


def login_required(func):
    return decorator(func, lambda u: u.is_authenticated)


def create_schema(props):
    required = []
    reqs = []
    for k, v in props.items():
        if isinstance(v, dict):
            if 'properties' in v:
                ret = dict(type="object", properties=v['properties'])
            if 'req' in v and v['req']:
                required.append(k)
            props[k], req = create_schema(v)
            if req:
                # print(props, req, '===============')
                reqs += req
    # print(props, required, '++++++++++++++')
    if reqs:
        props['required'] = reqs
    return props, required


def validate(*_properties):
    def inner(func):
        def inner2(cls, request, **kwargs):
            if 'json' in request.__dict__:
                data = request.json
            else:
                data = request.POST.dict()
            properties = dict(ChainMap(*_properties))
            properties, required = create_schema(properties)

            schema = dict(
                type="object",
                properties=properties,
                required=required
            )
            try:
                jsonschema.validate(data, schema)
                return func(cls, request, **kwargs)
            except jsonschema.exceptions.ValidationError as e:
                path = ''
                for i in e.path:
                    path += f'{i}.'
                raise AccessDenied(f'{path}{e.message}')
        return inner2
    return inner
