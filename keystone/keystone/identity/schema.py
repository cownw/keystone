import keystone.conf

CONF = keystone.conf.CONF


_identity_name = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 255,
    'pattern': r'[\S]+'
}

_user_properties = {
    'default_project_id': validation.nullable(parameter_types.id_string),
    
}