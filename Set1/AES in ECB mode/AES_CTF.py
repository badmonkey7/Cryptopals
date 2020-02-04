# coding=utf-8
from Crypto.Cipher import AES
from Crypto.
## 调用crypto中的函数封装自己的函数，更加高效
def AES_ECB_Encry(key,message):
    crypto = AES.new(key,AES.MODE_ECB)
    enc = crypto.encrypt(message)
    return enc

# 解密函数
def AES_ECB_Decry(key,enc):
    crypto = AES.new(key,AES.MODE_ECB)
    mess = crypto.decrypt(enc)
    return enc


keys = 'YELLOW SUBMARINE'

file = open('7.txt','r').read()
from base64 import b64decode
print AES_ECB_Decry(keys,b64decode(file))


