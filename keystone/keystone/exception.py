import http.client
from oslo_log import log
from oslo_utils import encodeutils

import keystone.conf
from keystone

CONF = keystone.conf.CONF
LOG = log.getLogger(__name__)

KEYSTONE_API_EXCEPTIONS = set([])

# Tests use this to make exception message format errors fatal
_FATAL_EXCEPTION_FORMAT_ERRORS = False


def _format_with_unicode_kwargs(msg_format, kwargs):
    try:
        return msg_format % kwargs
    except UnicodeDecodeError:
        try:
            kwargs = {k: encodeutils.safe_decode(v)
                      for k, v in kwargs.items()}
        except UnicodeDecodeError:
            # NOTE(jamielennox): This is the complete failure case
            # at least by showing the template we have some idea
            # of where the error is coming from
            return msg_format

        return msg_format % kwargs

class _KeystoneExceptionMeta(type):
    """Automatically Register the Exceptions in 'KEYSTONE_API_EXCEPTIONS' list.

    The `KEYSTONE_API_EXCEPTIONS` list is utilized by flask to register a
    handler to emit sane details when the exception occurs.
    """

    def __new__(mcs, name, bases, class_dict):
        """Create a new instance and register with KEYSTONE_API_EXCEPTIONS."""
        cls = type.__new__(mcs, name, bases, class_dict)
        KEYSTONE_API_EXCEPTIONS.add(cls)
        return cls


class Error(Exception, metaclass=_KeystoneExceptionMeta):
    """Base error class.

    Child classes should define an HTTP status code, title, and a
    message_format.

    """

    code = None
    title = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            # if you see this warning in your logs, please raise a bug report
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                LOG.warning('missing exception kwargs (programmer error)')
                message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Build and returns an exception message.

        :raises KeyError: given insufficient kwargs

        """
        if message:
            return message
        return _format_with_unicode_kwargs(self.message_format, kwargs)


class ValidationError(Error):
    message_format = _("Expecting to find %(attribute)s in %(target)s."
                       " The server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = int(http.client.BAD_REQUEST)
    title = http.client.responses[http.client.BAD_REQUEST]


class PasswordValidationError(ValidationError):
    message_format = _("Password validation error: %(detail)s.")
