import itertools

from oslo_log import log
import passlib.hash

import keystone.conf

CONF = keystone.conf.CONF
LOG = log.getLogger(__name__)

SUPPORTED_HASHERS = frozenset([passlib.hash.bcrypt,
                               passlib.hash.scrypt,
                               passlib.hash.pbkdf2_sha512,
                               passlib.hash.sha512_crypt])

_HASHER_IDENT_MAP = {
    prefix: module for module, prefix in itertools.chain(
        *[zip([mod] * len(getattr(mod, 'ident_values', (mod.ident,))),
              getattr(mod, 'ident_values', (mod.ident,)))
          for mod in SUPPORTED_HASHERS])}

def _get_hasher_from_ident(hashed):
    try:
        return _HASHER_IDENT_MAP[hashed[0:hashed.index('$', 1) + 1]]
    except KeyError:
        raise ValueError(
            _('Unsupported password hashing algorithm ident: %s') %
            hashed[0:hashed.index('$', 1) + 1])


def verify_length_and_trunc_password(password):
    """Verify and truncate the provided password to the max_password_length."""
    max_length = CONF.identity.max_password_length
    try:
        if len(password) > max_length:
            if CONF.strict_password_check:
                raise exception.PasswordVerificationError(size=max_length)
            else:
                msg = "Truncating user password to %d characters."
                LOG.warning(msg, max_length)
                return password[:max_length]
        else:
            return password
    except TypeError:
        raise exception.ValidationError(attribute='string', target='password')


def hash_user_password(user):
    """Hash a user dict's password without modifying the passed-in dict."""
    password = user.get('password')
    if password is None:
        return user
    
    return dict(user, password=hash_password(password))