def get_required(is_required):
    return {'req': is_required}


def make_object(x, _type, is_required=True, **kwargs):
    return {x: dict(type=_type, **get_required(is_required), **kwargs)}


def make_number_or_string_object(x, is_required=True):
    return make_object(x, ['string', 'number'], is_required)


def make_string_object(x, is_required=True):
    return make_object(x, "string", is_required)


def make_number_object(x, is_required=True):
    return make_object(x, "number", is_required)


def make_array_object(x, _type, is_required=True, **kwargs):
    return make_object(x, "array", is_required, items=dict(type=_type, **kwargs))


def make_email_object(x, is_required=True):
    return make_object(x, "string", is_required, pattern="^.*@.*\..*$")


def make_uri_object(x, is_required=True):
    return make_object(x, "string", is_required, pattern="^https?://.+")


def make_dict_object(x, is_required=True, **kwargs):
    return make_object(x, "object", is_required, **kwargs)


def make_boolean_object(x, is_required=True, **kwargs):
    return make_object(x, "boolean", is_required, **kwargs)
