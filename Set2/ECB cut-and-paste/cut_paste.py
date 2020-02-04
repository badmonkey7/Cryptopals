# coding=utf-8
import re
import os
from Crypto.Cipher import AES
def profile_for(string):
    string = string.replace('&','')
    string = string.replace('=','')
    return 'email='+string+'&uid=10&role=user'

def prasing_routine(string):
    all = re.findall('[\w]+=[\w@.]+', string)
    ans = {}
    for i in all:
        key,val = i.split('=')
        ans[key]=val
    return ans

def pad(s):
    bs = AES.block_size
    return s + chr(bs-len(s)%bs)*(bs-len(s)%bs)

def unpad(s):
    return s[0:-ord(s[-1])]

key = os.urandom(AES.block_size)
#
def oracle_encry(eamil):
    message = pad(profile_for(eamil))
    cipher = AES.new(key,AES.MODE_ECB)
    enc = cipher.encrypt(message)
    return enc

def oracle_decry(enc):
    cipher = AES.new(key,AES.MODE_ECB)
    mess = unpad(cipher.decrypt(enc))
    return mess

def decry(shell):
    bs = AES.block_size
    payload = 'a'*10+shell+chr(bs-len(shell)%bs)*(bs-len(shell)%bs)
    tot = len(shell)/bs +1
    admin_enc = oracle_encry(payload)[bs:bs+bs*tot]
    payload2 = '123456@qq.com'
    # 使得 role= 后面的单独成一块，并替换成admin_enc 达到目的
    enc = oracle_encry(payload2)
    bypass = enc[0:-bs]+admin_enc
    res = oracle_decry(bypass)
    return res

print decry('admin')
# 'email=123456@qq.com&uid=10&role='
# print oracle_decry(oracle_encry('1234567@qq.com'))

