# A couple common constants for Auth data

# Header used to transmit the auth token
AUTH_TOKEN_HEADER = 'X-Auth-Token'  # nosec


# Header used to transmit the auth receipt
AUTH_RECEIPT_HEADER = 'Openstack-Auth-Receipt'


# Header used to transmit the subject token
SUBJECT_TOKEN_HEADER = 'X-Subject-Token'  # nosec

# Environment variable used to convey the Keystone auth context,
# the user credential used for policy enforcement.
AUTH_CONTEXT_ENV = 'KEYSTONE_AUTH_CONTEXT'

# Header set by versions of keystonemiddleware that understand application
# credential access rules
ACCESS_RULES_HEADER = 'OpenStack-Identity-Access-Rules'
