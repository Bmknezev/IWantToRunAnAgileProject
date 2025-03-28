import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

#AES ECB mode without IV

def encrypt(raw, key):
        raw = pad(raw.encode(),16)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

def decrypt(enc, key):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16)


key = 'AAAAAAAAAAAAAAAA' #Must Be 16 char for AES128
encrypted = encrypt("Hello There", key)
print('encrypted ECB Base64:', encrypted.decode("utf-8", "ignore"))

decrypted = decrypt(encrypted, key)
print('data: ', decrypted.decode("utf-8", "ignore"))