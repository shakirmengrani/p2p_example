import msgpack
import json
from .crypto import Crypto

class Pack(object):

    def __init__(self, chunk):
        self.hash = Crypto()
        self.hash.saveKeyGen()
        self.chunk = chunk
    
    def encrypt(self, payload):
        return self.hash.encrypt(payload)

    def decrypt(self, payload):
        return self.hash.decrypt(payload)
    
    def serialize(self, enc):
        self.chunk.session_key = enc[0]
        self.chunk.nounce = enc[1]
        self.chunk.tag = enc[2]
        self.chunk.ciphertext = enc[3]
        self.chunk.private_key = self.hash.private_key
        self.chunk.public_key = self.hash.public_key
        return self.chunk.SerializeToString()
    
    def unserialize(self, chunk):
        self.hash.private_key = chunk.private_key
        self.hash.public_key = chunk.public_key
        return chunk.session_key, chunk.nounce, chunk.tag, chunk.ciphertext, chunk.private_key, chunk.public_key

    def pack(self, data):
        serialize = self.serialize(self.hash.encrypt(data))
        return msgpack.packb(serialize, use_bin_type=False)
    
    def unpack(self, data):
        binU = msgpack.unpackb(data, raw=True)
        self.chunk.ParseFromString( binU )
        return self.decrypt(self.unserialize(self.chunk))

# p = Pack()
# packed_text = p.pack(json.dumps({
#     "filename": "shakir mengrani",
#     "pieces": [1,2,3]
# }))
# unpacked_text = p.unpack(packed_text)
# print(unpacked_text)