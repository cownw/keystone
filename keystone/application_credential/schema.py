from keystone.common import validation
from keystone.common.validation import parameter_types

_role_properties = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': parameter_types.id_string,
            'name': parameter_types.name
        },
        'minProperties': 1,
        'maxProperties': 1,
        'additionalProperties': False
    }
}