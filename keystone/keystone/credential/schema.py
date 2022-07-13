
_credential_properties = {
    'blob': {
        'type': 'string'
    },
    'project_id': {
        'type': 'string'
    },
    'type': {
        'type': 'string'
    },
    'user_id': {
        'type': 'string'
    }
}

credential_create = {
    'type': 'object',
    'properties': _credential_properties,
    'additionalProperties': True,
    'oneOf': [
        {
            'title': 'ec2 credential requires project_id',
            'required': ['blob', 'type', 'user_id', 'project_id'],
            'properties': {
                'type': {
                    'enum': ['ec2']
                }
            }
        },
        {
            'title': 'non-ec2 credential does not require project_id',
            'required': ['blob', 'type', 'user_id'],
            'properties': {
                'type': {
                    'not': {
                        'enum': ['ec2']
                    }
                }
            }
        }
    ]
}

credential_update = {
    'type': 'object',
    'properties': _credential_properties,
    'minProperties': 1,
    'additionalProperties': True
}
