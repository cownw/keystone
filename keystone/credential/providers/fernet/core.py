import hashlib

from cryptography import fernet
from oslo_log import log

import keystone.conf

CONF = keystone.conf.CONF
LOG = log.getLogger(__name__)


