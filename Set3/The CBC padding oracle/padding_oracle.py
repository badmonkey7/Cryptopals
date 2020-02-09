# coding=utf-8
from random import randint
import os
from Crypto.Cipher import AES
from base64 import b64decode
all = [
"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]
#
key = os.urandom(16)
#
pad = lambda s: s+chr(16-len(s)%16)*(16-len(s)%16)
#
unpad = lambda s: s[-ord(s[-1]):] == chr(ord(s[-1]))*ord(s[-1])
#
def oracle():
    m = b64decode(all[randint(0, 9)])
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    enc = cipher.encrypt(pad(m))
    return iv+enc
#
def check_oracle(enc):
    iv = enc[0:AES.block_size]
    cipher = AES.new(key,AES.MODE_CBC,iv)
    mess = cipher.decrypt(enc[AES.block_size:])
    # res = unpad(mess)
    # print res[1]
    return unpad(mess)
##############################################
def xor(a,b):
    return ''.join([chr(ord(i)^ord(j)) for i,j in zip(a,b)])
# 注意事项 可能有多个合法padding，需要处理，我的解决方法不太好当是也能凑合用，即记录下所有可能，找出一种合法的即可
def judge(bs,tmp,enc,pos):
    if pos == bs:
        return [True,''.join(tmp)]
    for i in range(pos,bs):
        j = 0
        nxt = ''
        for k in range(i, 0, -1):
            nxt += chr(ord(tmp[-k]) ^ (i + 1))
        record = []
        while j < 256:
            payload = chr(0) * (bs - i - 1) + chr(j) + nxt
            if check_oracle(payload + enc):
                record.append(chr(j ^ (i + 1)))
            j += 1
        # 非法，可能是因为之前猜测的结果错误的原因
        if len(record) == 0:
            return [False,'']
        elif len(record) == 1:
            # 只有一种可能不用调用函数
            tmp[-i-1] = record[0]
        else:
            # 尝试所有可能性
            for k in record:
                tmp[-i-1] = k
                res = judge(bs,tmp,enc,i+1)
                # 合法的可能 直接返回，不合法的不考虑
                if res[0]:
                    return [True, res[1]]
    return [True,''.join(tmp)]

#
#
# 一块一块暴力破解
def padding_oracle_block(iv,bs,enc):
    tmp = ['']*bs
    res = judge(bs,tmp,enc,0)[1]
    return xor(iv,res)

def padding_oracle():
    enc = oracle()
    bs = AES.block_size
    iv = enc[0:bs]
    blocks = [enc[bs*i:bs*i+bs] for i in range(1,len(enc[bs:])/bs)]
    message = ''
    for block in blocks:
        try:
            message += padding_oracle_block(iv,bs,block)
        except:
            f = open('log.txt','w+')
            log = "iv == "+iv.encode('hex')+'\n'+"key == "+key.encode('hex')+'\n'+'block=='+block.encode('hex')+'\n'
            f.write(log)
            f.close()
            return 'error please check your logs to see more details'
        # print message
        iv = block
    return message

print padding_oracle()







