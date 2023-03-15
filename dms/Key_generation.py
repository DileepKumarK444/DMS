import random
import string
import pgpy
from pgpy.constants import (
    PubKeyAlgorithm, KeyFlags, HashAlgorithm,
    SymmetricKeyAlgorithm, CompressionAlgorithm)
from enum import Enum
import secrets


class random_key:
    def __init__(self, stringLength=None):
        self.keylen = stringLength
        self.key = self.create()

    def create(self):
        if not self.keylen:
            return 'Enter key size'
        # lettersAndDigits = string.ascii_letters + string.digits
        # return ''.join((random.choice(lettersAndDigits) for i in range(self.keylen)))
        return secrets.token_hex(self.keylen)  


class pgpy_key:
    def __init__(self, name='', email=''):
        self.name = name
        self.email = email
        self.prikey, self.pubkey = self.create()

    def create(self):
        # we can start by generating a primary key. For this example, we'll use RSA, but it could be DSA or ECDSA as well
        key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)

        # we now have some key material, but our new key doesn't have a user ID yet, and therefore is not yet usable!
        uid = pgpy.PGPUID.new(self.name, email=self.email)

        # now we must add the new user id to the key. We'll need to specify all of our preferences at this point
        key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                    hashes=[HashAlgorithm.SHA256],
                    ciphers=[SymmetricKeyAlgorithm.AES256, ],
                    compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP, CompressionAlgorithm.Uncompressed])
        # protect privatekey with passcode(used name instead)
        if self.name:
            key.protect(self.name, SymmetricKeyAlgorithm.AES256,
                        HashAlgorithm.SHA256)
        return key, key.pubkey


# a = random_key(32)
# print(a.key)

# a = pgpy_key('')
# print((a.prikey), (a.pubkey))

# import uuid

# print(uuid.uuid1())
