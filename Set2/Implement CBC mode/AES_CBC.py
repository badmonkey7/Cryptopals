# coding=utf-8
import base64
from data import s, rs, Rcon


# key块 为四位字符串
# S 盒转化
def S(key):
    ans = ''
    for i in key:
        tmp = "0x" + "{:02x}".format(ord(i))
        ans += chr(int(s[tmp], 16))
    return ans


# 逆S盒转化
def RS(key):
    ans = ''
    for i in key:
        tmp = "0x" + "{:02x}".format(ord(i))
        ans += chr(int(rs[tmp], 16))
    return ans


# T 函数,对key进行处理，order为第几轮处理
def T(key, order):
    # 循环左移
    key += key[0]
    key = key[1:]
    # S 盒转化
    key = S(key)
    # 异或运算
    key = list(key)
    for i in range(len(key)):
        key[i] = chr(ord(key[i]) ^ int(Rcon[order][i], 16))
    key = ''.join(key)
    return key


# 密钥块之间进行异或运算
def xor(a, b):
    a = list(a)
    b = list(b)
    for i in range(len(a)):
        a[i] = chr(ord(a[i]) ^ ord(b[i]))
    a = ''.join(a)
    return a


# keys 为16位密钥字符串，返回44 bytes的扩展key
def key_ext(keys):
    W = []
    cur = ''
    # 初始 密钥划成4份
    for i in range(0, len(keys), 4):
        cur = ''.join(keys[i:i + 4])
        W.append(cur)
    # 十轮密钥
    pos = 4
    for i in range(40):
        t1 = W[pos - 4]
        if pos % 4 == 0:
            # 被四整除 特殊处理
            t2 = T(W[pos - 1], i / 4)
        else:
            t2 = W[pos - 1]
        tmp = xor(t1, t2)
        W.append(tmp)
        pos += 1
    return W


# 轮密匙加,mess 为待加密信息，cir为加密轮数,从0开始
def cir_key_add(mess, cir, W):
    res = ''
    for i in range(4):
        res += xor(mess[4 * i:4 * i + 4], W[4 * cir + i])
    return res


# 行位移,mess为需要位移的16为字符串
def row_change(mess):
    mess = list(mess)
    ans = ''
    for i in range(0, 16, 4):
        for j in range(4):
            ans += mess[(i + 5 * j) % 16]
    return ans


# 逆行移位
def re_row_change(mess):
    ans = mess[0] + mess[13] + mess[10] + mess[7]
    ans += mess[4] + mess[1] + mess[14] + mess[11]
    ans += mess[8] + mess[5] + mess[2] + mess[15]
    ans += mess[12] + mess[9] + mess[6] + mess[3]
    return ans


# 有限域 乘法递归实现,加法相当于异或
def muti(a, b):
    t = 0
    res = 0
    if a == 2:
        tag = "{:08b}".format(b)
        if tag[0] == '0':
            res = int(tag[1:] + '0', 2)
        else:
            res = int(tag[1:] + '0', 2) ^ int('00011011', 2)
    elif a == 1:
        res = b
    else:
        cur = 1
        cnt = 0
        while cur <= a:
            cnt += 1
            cur *= 2
        cur /= 2
        cnt -= 1
        r = (a - cur)
        t = muti(2, b)
        for i in range(cnt-1):
            t = muti(2, t)
        if r != 0:
            res = t ^ muti(r, b)
        else:
            res = t
    # print res,
    return res


# 列混合，有限域上的运算
def col_mix(mess):
    mess = list(mess)
    ans = ''
    # print "列混合前:"+''.join(mess).encode('hex')
    for i in range(0, len(mess), 4):
        cur = mess[i:i + 4]
        ans += chr(muti(2, ord(cur[0])) ^ muti(3, ord(cur[1])) ^ ord(cur[2]) ^ ord(cur[3]))
        # print muti(2, ord(cur[0])) ^ muti(3, ord(cur[1])) ^ ord(cur[2]) ^ ord(cur[3]),
        ans += chr(ord(cur[0]) ^ muti(2, ord(cur[1])) ^ muti(3, ord(cur[2])) ^ ord(cur[3]))
        # print ord(cur[0]) ^ muti(2, ord(cur[1])) ^ muti(3, ord(cur[2])) ^ ord(cur[3]),
        ans += chr(ord(cur[0]) ^ ord(cur[1]) ^ muti(2, ord(cur[2])) ^ muti(3, ord(cur[3])))
        # print ord(cur[0]) ^ ord(cur[1]) ^ muti(2, ord(cur[2])) ^ muti(3, ord(cur[3])),
        ans += chr(muti(3, ord(cur[0])) ^ ord(cur[1]) ^ ord(cur[2]) ^ muti(2, ord(cur[3])))
        # print muti(3, ord(cur[0])) ^ ord(cur[1]) ^ ord(cur[2]) ^ muti(2, ord(cur[3])),
    # print "列混合后："+ans.encode('hex')
    return ans


# 逆列混合运算
def re_col_mix(mess):
    mess = list(mess)
    # print "列混合后"+''.join(mess).encode('hex')
    ans = ''
    for i in range(0, len(mess), 4):
        cur = mess[i:i + 4]
        ans += chr(
            muti(0x0e, ord(cur[0])) ^ muti(0x0b, ord(cur[1])) ^ muti(0x0d, ord(cur[2])) ^ muti(0x09, ord(cur[3])))
        # print muti(0x0e, ord(cur[0])) ^ muti(0x0b, ord(cur[1])) ^ muti(0x0d, ord(cur[2])) ^ muti(0x09, ord(cur[3])),
        ans += chr(
            muti(0x09, ord(cur[0])) ^ muti(0x0e, ord(cur[1])) ^ muti(0x0b, ord(cur[2])) ^ muti(0x0d, ord(cur[3])))
        # print muti(0x09, ord(cur[0])) ^ muti(0x0e, ord(cur[1])) ^ muti(0x0b, ord(cur[2])) ^ muti(0x0d, ord(cur[3])),
        ans += chr(
            muti(0x0d, ord(cur[0])) ^ muti(0x09, ord(cur[1])) ^ muti(0x0e, ord(cur[2])) ^ muti(0x0b, ord(cur[3])))
        # print muti(0x0d, ord(cur[0])) ^ muti(0x09, ord(cur[1])) ^ muti(0x0e, ord(cur[2])) ^ muti(0x0b, ord(cur[3])),
        ans += chr(
            muti(0x0b, ord(cur[0])) ^ muti(0x0d, ord(cur[1])) ^ muti(0x09, ord(cur[2])) ^ muti(0x0e, ord(cur[3])))
        # print muti(0x0b, ord(cur[0])) ^ muti(0x0d, ord(cur[1])) ^ muti(0x09, ord(cur[2])) ^ muti(0x0e, ord(cur[3])),
    # print "列混合前："+ans.encode('hex')
    return ans
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
    return record

# remove pkcs7padding
def removePkcs7(target):
    lst = target[-1]
    pos = 0
    for i in range(len(target)-1,-1,-1):
        if target[i] != lst:
            pos = i+1
            break
    return target[0:pos]

# AES_128_ECB 加密，采用pkcs5padding方式填充
def AES_128_CBC(message, keys,iv):
    # 先进行分组，128位一组
    record = pkcs7padding(message,16)
    enc = ''
    # 密钥扩展
    W = key_ext(keys)
    # 对每一组进行加密,先和前驱密钥异或
    pre = iv
    for mess in record:
        # print '第0轮加密....','加密前:'+mess.encode('hex'),
        mess = xor(mess,pre)
        # 初始的 密钥加
        mess = cir_key_add(mess, 0, W)
        # print '加密后', mess.encode('hex')
        # 十轮加密
        # 前九轮
        for i in range(0, 9):
            # print "第{}轮加密....".format(i + 1),'加密前:'+mess.encode('hex'),
            # 字节代换
            mess = S(mess)
            # 行位移
            mess = row_change(mess)
            # 列混合
            mess = col_mix(mess)
            # 轮换密匙加
            mess = cir_key_add(mess, i + 1, W)
            # print "加密后:".format(i + 1), mess.encode('hex')
        # 第十轮加密
        # print "第10轮加密...",'加密前:'+mess.encode('hex'),
        mess = S(mess)
        mess = row_change(mess)
        mess = cir_key_add(mess, 10, W)
        pre = mess
        # print "加密后:", mess.encode('hex')
        enc += mess
    return enc

# 128 位 的块解密
def decry_block(block,W):
    i = block
    # 第一轮
    # print '解密第10轮', '解密前:' + i.encode('hex'),
    i = cir_key_add(i, 10, W)
    i = re_row_change(i)
    i = RS(i)
    # print '解密后:', i.encode('hex')
    # 后续九轮
    for r in range(9, 0, -1):
        # print '解密第{}轮'.format(r), "解密前:" + i.encode('hex'),
        i = cir_key_add(i, r, W)
        i = re_col_mix(i)
        i = re_row_change(i)
        i = RS(i)
        # print '解密后:', i.encode('hex')
    # print '解密第0轮', "解密前:" + i.encode('hex'),
    i = cir_key_add(i, 0, W)
    # print '解密后:', i.encode('hex')
    return i
# 解密
def decry_AES_128_CBC(enc, key,iv):
    # 密钥扩展
    W = key_ext(key)
    # 先进行分组，128位一组
    tot = len(enc) // 16
    record = []
    for i in range(0, tot):
        record.append(enc[16 * i: 16 * i + 16])
    message = ''
    if len(record) == 1:
        i = record[0]
        i = decry_block(i, W)
        # 解密之后与iv异或
        i = xor(i,iv)
        # remove padding
        i = removePkcs7(i)
        message = i
    else:
        pre = iv
        for i in range(0,len(record)-1):
            block = record[i]
            cur = decry_block(block,W)
            message += xor(pre,cur)
            pre = block
        # 最后一块，特殊处理
        lst = xor(pre,decry_block(record[-1],W))
        # remove padding
        message += removePkcs7(lst)
    return message


keys = 'YELLOW SUBMARINE'
mess = 'happy_2020aaaaaaaaaa'
# t = 't8is_Is a teSt!!'
iv = ''
for i in range(16):
    iv += chr(0)
file = open('10.txt','r').read()
from base64 import b64decode
file = b64decode(file)
passage = decry_AES_128_CBC(file,keys,iv)
print passage
