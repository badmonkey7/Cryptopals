# coding=utf-8
from base64 import b64decode
import string
import os
from random import randint
from Crypto.Cipher import AES

# actually in the simple part i have consider the offside (the prefix byte)
# so i just copy my previous code and made some small changes

# global key
key = os.urandom(16)
# prefix
prefix = os.urandom(randint(5,10))
# padding
def pkcs7(s,bs):
    return s+chr(bs-len(s)%bs)*(bs-len(s)%bs)

# api encrypt
def oracle(message):
    add = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    unknown = b64decode(add)
    message = prefix+'{}'.format(message)+unknown
    message = pkcs7(message,AES.block_size)
    cipher = AES.new(key,AES.MODE_ECB)
    enc = cipher.encrypt(message)
    return enc

# find the offside
def find_offside():
    bs = find_block_size()
    # offside = k*block_size + m => offside = m(mod block_size)
    enc = oracle('')
    length = len(enc)
    if length == 0:
        return 0
    record = [enc[i*bs:bs*i+bs] for i in range(length/bs)]
    for i in range(bs):
        message = i*'A'+'A'*bs*2
        cur = oracle(message)
        tmp = [cur[bs*j:bs*j+bs] for j in range(len(cur)/bs)]
        # detected offside
        pos = -1
        # find the first different encrypt block
        for j in range(len(record)):
            if tmp[j] != record[j]:
                pos = j
                break
        if pos == -1:
            return length
        else:
            if pos == len(record)-1:
                if tmp[pos+1] == tmp[pos+2]:
                    return (pos+1)*bs-i
            else:
                if tmp[pos + 1] == tmp[pos + 2]:
                    if tmp[pos+3] == record[pos+1]:
                        return (pos+1)*bs
                    else:
                        return (pos+1)*bs -i
    return 0


## find the block size in aes
def find_block_size():
    block_size = 0
    cur = 0
    for i in range(0,32):
        tmp = len(oracle('A'*i))
        if cur == 0:
            cur = tmp
            continue
        elif tmp > cur:
            block_size = tmp -cur
            break
    return block_size
# judge if this is aes ecb mode
def detect_ecb():
    bs = find_block_size()
    enc = oracle('A'*bs*5)
    record = [enc[i*bs:i*bs+bs] for i in range(len(enc)/bs)]
    for i in record:
        if record.count(i)>1:
            return True
    return False
# single block encry
def pure_oracle(string,bs=find_block_size(),off=find_offside()):
    if off%bs:
        length = off / bs +1
    else:
        length = off /bs
    mess = (length*bs-off)*'A'+string
    enc = oracle(mess)[length*bs:length*bs+bs]
    return enc

# brute force
def find_fir_diff(bs,off,pad):
    enc = oracle('')
    record = [enc[i*bs:i*bs+bs] for i in range(len(enc)/bs)]
    if off%bs:
        length = off / bs +1
    else:
        length = off /bs
    cur = oracle(pad*(length*bs-off+bs))
    tmp = [cur[i*bs:i*bs+bs] for i in range(len(cur)/bs)]
    pos = -1
    for i in range(len(record)):
        if tmp[i] != record[i]:
            pos = i+1
            break
    num = len(record)-pos
    return [pos,num]


# find the unknown string
def decry_ecb():
    bs = find_block_size()
    off = find_offside()
    if detect_ecb():
        [start,tot] = find_fir_diff(bs,off,'A')
        pre = bs - off % bs
        # total bytes
        plain = 'A'*bs
        all = string.printable
        for byte in range(tot+1):
            cur = pre * 'A'
            pos = start+byte
            # attack every bit
            record = list(plain[-bs+1:]+plain[-bs])
            nt = ''
            for bit in range(bs):
                payload = cur +(bs-bit-1)*'A'
                enc = oracle(payload)[pos*bs:pos*bs+bs]
                for item in all:
                    record[-1] = item
                    tmp = ''.join(record)
                    if pure_oracle(tmp) == enc:
                        nt = tmp[-bit-1:]
                        tmp = tmp[1:] + tmp[0]
                        record = list(tmp)
                        break
            plain += nt
        plain = plain[bs:]
        return plain
    else:
        return ''


print decry_ecb()