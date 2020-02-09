from Crypto.Cipher import AES
from Crypto.Util import Counter
from base64 import b64decode
import os
key = os.urandom(16)
###############################################
# def CTR(m):
#     ctr = Counter.new(128)
#     cipher = AES.new(key,AES.MODE_CTR,counter=ctr)
#     enc = cipher.encrypt(m)
#     return enc
# use pycrypto to do this job is really simple
###############################################
nonce = chr(0)*8
#
xor = lambda a,b: ''.join([chr(ord(a[i])^ord(b[i])) for i in range(min(len(a),len(b)))])
#
def CTR_Encry(m):
    bs = AES.block_size
    cipher = AES.new(key,AES.MODE_ECB)
    stream = ''
    for i in range(len(m)/bs+1):
        ctr = nonce + chr(i)+chr(0)*7
        stream += cipher.encrypt(ctr)
    return xor(m,stream)
# encry and decry use the same function
m = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
print CTR_Encry(CTR_Encry(b64decode(m)))


