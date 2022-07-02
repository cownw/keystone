import abc


class Provider(object, metaclass=abc.ABCMeta):
    """Interface for credential providers that support encryption."""

    @abc.abstractmethod
    def encrypt(self, credential):
        """Encrypt a credential.

        :param str credential: credential to encrypt
        :returns: encrypted credential str
        :raises: keystone.exception.CredentialEncryptionError
        """

    @abc.abstractmethod
    def decrypt(self, credential):
        """Decrypt a credential.

        :param str credential: credential to decrypt
        :returns: credential str as plaintext
        :raises: keystone.exception.CredentialEncryptionError
        """
