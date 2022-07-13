"""Translation function factory
"""

from oslo_i18n import _message

__all__ = [
    'TranslatorFactory',
]

# magic gettext number to separate context from message
CONTEXT_SEPARATOR = _message.CONTEXT_SEPARATOR

class TranslatorFactory(object):
    "Create translator functions"

    def __init__(self, domain, localedir=None):
        """Establish a set of translation functions for the domain.

        :param domain: Name of translation domain,
                       specifying a message catalog.
        :type domain: str
        :param localedir: Directory with translation catalogs.
        :type localedir: str
        """
        self.domain = domain
        if localedir is None:
            variable_name = _l
