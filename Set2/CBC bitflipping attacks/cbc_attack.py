import os
from Crypto.Cipher import AES
#
pad = lambda s:s+(AES.block_size-len(s)%AES.block_size)*chr(AES.block_size-len(s)%AES.block_size)
#
unpad = lambda s:s[0:-ord(s[-1])]
# key
key = os.urandom(AES.block_size)
# iv
iv = os.urandom(AES.block_size)
#
def cbc_encry(m):
    # replace ; and =
    m = m.replace(';','')
    m = m.replace('=','')
    pre = "comment1=cooking%20MCs;userdata="
    nxt = ";comment2=%20like%20a%20pound%20of%20bacon"
    m = pad(pre+m+nxt)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    enc = cipher.encrypt(m)
    return enc

# check if there is admin in message
def check(enc,target='admin=true'):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    mess = unpad(cipher.decrypt(enc))
    record = mess.split(';')
    for item in record:
        if target in item:
            print mess
            return True
    return False

# bit flipping attack
# comment1=cooking%20MCs;userdata= bbbbbbadminbtrue ;comment2=%20like%20a%20pound%20of%20bacon
def attack():
    payload = 'bbbbbbadminbtrue'
    enc = cbc_encry(payload)
    bs = AES.block_size
    enc = list(enc)
    # bit flipping attack
    enc[21] = chr(ord(enc[21])^ord(payload[5])^ord(';'))
    enc[27] = chr(ord(enc[27])^ord(payload[11])^ord('='))
    enc = ''.join(enc)
    if check(enc):
        return 'attack success'
    else:
        return 'attack fail'

print attack()
