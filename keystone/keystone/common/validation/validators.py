"""Internal implementation of request body validating middleware."""

import re

import jsonschema
from oslo_config import cfg

CONF = cfg.CONF

def validate_password(password):
    pattern = CONF.security_compliance.password_regex
    if pattern:
        if not isinstance(password, str):
            detail = _("Password must be a string type")
            raise exception.