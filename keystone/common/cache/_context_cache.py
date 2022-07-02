"""A dogpile.cache proxy that caches objects in the request local cache."""
from dogpile.cache import api
from dogpile.cache import proxy
from oslo_context import context as oslo_context
from oslo_serialization import msgpackutils

_registry = msgpackutils.default_registry

def _registry_model_handler(handler_class):
    """Registry a new model handler."""
    _registry.frozen = False
    _registry.register(handler_class(registry=_registry))
    _registry.frozen = True


class _ResponseCacheProxy(proxy.ProxyBackend):

    __key_pfx = '_request_cache_%s'

    def _get_request_context(self):
        # Return the current context or a new/empty context.
        return oslo_context.get_current() or oslo_context.RequestContext()

    def _get_request_key(self, key):
        return self.__key_pfx % key

    def _set_local_cache(self, key, value):
        # Set a serialized version of the returned value in local cache for
        # subsequent calls to the memoized method.
        ctx = self._get_request_context()
        serialize = {'payload': value.payload, 'metadata': value.metadata}
        setattr(ctx, self._get_request_key(key), msgpackutils.dumps(serialize))

    def _get_local_cache(self, key):
        ctx = self._get_request_context()
        try:
            value = getattr(ctx, self._get_request_key(key))
        except AttributeError:
            return api.NO_VALUE

        value = msgpackutils.load(value)
        return api.CachedValue(payload=value['payload'],
                                metadata=value['metadata'])
                                