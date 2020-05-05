def get_required(is_required):
    return {'required': is_required}


def make_string_object(x, is_required=True):
    return {x: dict(type="string", **get_required(is_required))}


def make_number_object(x, is_required=True):
    return {x: dict(type="number", **get_required(is_required))}


def make_array_object(x, _type, is_required=True):
    return {x: dict(type="array", items=dict(type=_type), **get_required(is_required))}
