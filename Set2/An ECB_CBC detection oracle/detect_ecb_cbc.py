# coding=utf-8
from random import randint
from AES_CBC_CTF import pkcs7padding,removepkcs7padding
from AES_ECB import AES_128_ECB
from AES_CBC import AES_128_CBC
# 产生随机的 size位字符串
def generate_random(size):
    res = ''
    for i in range(size):
        res += chr(randint(0,255))
    return res
# 加密算法
def encryption_oracle(mess):
    # 生成随机16位密钥
    key = generate_random(16)
    # 信息 添加前后缀
    front = generate_random(randint(5,10))
    back = generate_random(randint(5,10))
    # 添加 padding
    mess = pkcs7padding(front+mess+back,16)
    # 随机选择ecb，cbc进行加密
    d = randint(0,1)
    if d==0:
        mess = AES_128_ECB(mess,key)
    else:
        iv = generate_random(16)
        mess = AES_128_CBC(mess,key,iv)
    return mess

# 探测加密方式
def detect_ecb_cbc(enc):
    record = [enc[16*i:16*i+16] for i in range(0,len(enc)/16)]
    for i in record:
        if record.count(i)>1:
            return 'ECB MODE Detected!!'
    return 'CBC MODE Detected!!'

mess = 'this is a test,it has taken a lot of time but i really enjoying the process!'*6
enc = encryption_oracle(mess)
print detect_ecb_cbc(enc)



