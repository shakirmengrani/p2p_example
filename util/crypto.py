from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class Crypto(object):
    def __init__(self, fileParam = {}, key_bytes=2048, session_bytes=16):
        self.session_key = fileParam["session_key"] if len(fileParam) > 1 else None
        self.private_key = fileParam["private_key"] if len(fileParam) > 1 else None
        self.public_key = fileParam["public_key"] if len(fileParam) > 1 else None 
        self.inFile = True if len(fileParam) > 1 else False
        self.key_bytes = key_bytes 
        self.session_bytes = session_bytes
         
    def writeFile(self, filename, payload):
        with open(filename, "wb") as fp:
            fp.write(payload)
            fp.close()
    
    def readKey(self, key, inFile):
        return open(key, 'rb').read() if inFile else key 

    def keyGen(self, key_bytes=2048, session_bytes=16):
        key = RSA.generate(key_bytes)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return get_random_bytes(session_bytes), private_key, public_key
    
    def saveKeyGen(self):
        session_key, private_key, public_key = self.keyGen(self.key_bytes, self.session_bytes)
        if self.inFile:
            self.writeFile(self.session_key, session_key)
            self.writeFile(self.private_key, private_key)
            self.writeFile(self.public_key, public_key)
        else:
            self.session_key = session_key
            self.private_key = private_key if self.private_key is None else self.private_key
            self.public_key = public_key if self.public_key is None else self.public_key

    def encrypt(self, payload):
        recipient_key = RSA.import_key(self.readKey(self.public_key, self.inFile))
        cipher_rsa = PKCS1_OAEP.new(recipient_key)  
        enc_session_key = cipher_rsa.encrypt(self.session_key)
        cipher_aes = AES.new(self.session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(payload.encode())
        return enc_session_key, cipher_aes.nonce, tag, ciphertext

    def decrypt(self, params):
        private_key = RSA.import_key(self.readKey(self.private_key, self.inFile))
        enc_session_key = params[0]
        nonce = params[1]
        tag = params[2]
        ciphertext = params[3]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode()


if "__main__" == __name__:
    '''
    fileDict = {
        "session_key": "session.txt",
        "private_key": "private.pem",
        "public_key": "public.pem"
    }
    '''
    hash = Crypto()
    hash.saveKeyGen()
    enc_data = hash.encrypt("Hello World")
    data = hash.decrypt(enc_data)
    print(enc_data)
    print(data)
