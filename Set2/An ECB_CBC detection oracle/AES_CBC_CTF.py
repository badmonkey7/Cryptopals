# coding=utf-8
from Crypto.Cipher import AES

# pkcs 7 padding
def pkcs7padding(target,size):
    tot = len(target)//size
    record = []
    if tot :
        for i in range(tot):
            record.append(target[i*size:i*size + size])
    pad = tot*size+size-len(target)
    if pad != 0:
        record.append(target[tot*size:]+chr(pad)*pad)
    else:
        record.append(chr(size)*size)
    return ''.join(record)
# remov pkcs7 padding
def removepkcs7padding(target,size):
    record = [target[i*size:i*size+size] for i in range(0,len(target)/size)]
    lst = record[-1]
    tag = lst[-1]
    pos = 0
    for i in range(len(lst)-1,-1,-1):
        if lst[i] != tag:
            pos = i+1
            break
    record[-1] = lst[0:pos]
    return ''.join(record)

# CBC 加密
def AES_CBC_Enc(mess,key,iv):
    mess = pkcs7padding(mess,AES.block_size)
    crypto = AES.new(key,AES.MODE_CBC,iv)
    enc = crypto.encrypt(mess)
    return enc

# CBC 解密
def AES_CBC_Decry(enc,key,iv):
    crypto = AES.new(key,AES.MODE_CBC,iv)
    message = crypto.decrypt(enc)
    message = removepkcs7padding(message,AES.block_size)
    return message

# keys = 'YELLOW SUBMARINE'
# mess = 'happy_2020aaaaaaaaaaasdf'
# iv = '1234567890abcdef'
#
# print AES_CBC_Decry(AES_CBC_Enc(mess,keys,iv),keys,iv)
