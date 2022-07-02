"""Request body validating middleware for OpenStack Identity resources."""

def lazy_validation(request_body_schema, resource_to_validate):
    """A non-decorator way to validate a request, to be used inline.
    
    :param request_body_schema: a schema to validate the resource reference
    :param resource_to_validate: dictionary to validate
    :raises keystone.exception.ValidationError: if `
    """
    schema_validator = va