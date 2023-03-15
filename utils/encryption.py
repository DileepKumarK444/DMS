from Crypto.Cipher import AES
import base64
import codecs
# import pgpy

BS = 16


def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def unpad(s): return s[0:-s[-1]]


class aes:

    def __init__(self, key, iv=None):

        self.key = key.encode('utf8')
        if iv:
            self.iv = iv.encode('utf-8')
        else:
            self.iv = iv

    def encrypt(self, raw):
        raw = pad(raw).encode('utf8')
        if self.iv:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw)).decode('utf8')

    def decrypt(self, enc):

        enc = base64.b64decode(enc)
        if self.iv:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        a = cipher.decrypt(enc)
        return unpad(a).decode('utf8')

    def decrypt_hexa(self, enc):
        enc = codecs.encode(codecs.decode(
            enc, 'hex'), 'base64').decode()

        enc = base64.b64decode(enc)
        if self.iv:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        a = cipher.decrypt(enc)
        return unpad(a).decode('utf8')

    def encrypt_file(self, from_file_name):
        with open(from_file_name, 'rb') as fo:
            plaintext = fo.read().decode('utf8')
        raw = pad(plaintext).encode('utf8')
        if self.iv:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        enc = base64.b64encode(cipher.encrypt(
            raw)).decode('utf8')
        with open(from_file_name + ".en", 'wb') as fo:
            fo.write(enc)
        return enc

    def decrypt_file(self, to_file_name):
        with open(to_file_name, 'rb') as fo:
            ciphertext = fo.read()
        ciphertext = base64.b64decode(ciphertext)
        if self.iv:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        a = unpad(cipher.decrypt(ciphertext))
        with open(to_file_name, 'wb') as fo:
            fo.write(a)
        return to_file_name

    def decrypt_file_hexa(self, to_file_name):
        with open(to_file_name, 'rb') as fo:
            ciphertext = fo.read()
        ciphertext = codecs.encode(codecs.decode(
            ciphertext, 'hex'), 'base64').decode()
        ciphertext = base64.b64decode(ciphertext)
        if self.iv:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.key, AES.MODE_ECB)
        a = unpad(cipher.decrypt(ciphertext))
        with open(to_file_name, 'wb') as fo:
            fo.write(a)
        return to_file_name


# class pgp:
#     def __init__(self, prikey=None, pubkey=None, passphrase=None):
#         self.pubkey, _ = pgpy.PGPKey.from_blob(pubkey)
#         self.prikey, _ = pgpy.PGPKey.from_blob(prikey)
#         self.passphrase = passphrase

#     def encrypt(self, data):
#         message = pgpy.PGPMessage.new(data)
#         enc_message = self.pubkey.encrypt(message)
#         encrypted = bytes(enc_message)
#         return encrypted.decode("utf8")

#     def decrypt(self, data):
#         message = pgpy.PGPMessage.from_blob(data)
#         if len(self.passphrase) != 0:
#             with self.prikey.unlock(self.passphrase):
#                 decrypted = self.prikey.decrypt(message).message
#         else:
#             decrypted = self.prikey.decrypt(message).message
#         return decrypted

#     def decrypt_file(self, file_name, file_type=None):
#         with open(file_name, 'rb') as fo:
#             try:
#                 if file_type == "pgp":
#                     ciphertext = fo.read()
#                 elif file_type == "txt":
#                     ciphertext = fo.read().decode('utf8')
#             except Exception as e:
#                 return "Decryption/Decode Error:" + str(e)
#         dec = self.decrypt(ciphertext)
#         try:

#             with open(file_name, 'w') as fo:
#                 fo.write(dec)
#         except:
#             with open(file_name, 'wb') as fo:
#                 fo.write(dec)
