# coding=utf-8
from base64 import decode
from signle_byte_attack import single_byte_attack,calScore
import itertools

# 异或之后统计1的数目
def edit_dis(a, b):
    cnt = 0
    for i in range(0, min(len(a), len(b))):
        cnt += bin(ord(a[i]) ^ ord(b[i])).count('1')
    return cnt

# keysize选择的方式要根据 平均编辑距离选择！，num 为选择的块数，块数越多越精准，时间也越长
def guess_keysize(a,num=4):
    record = []
    val = []
    for i in range(2, 40):
        # 每 i 个分成一组，取两组之间计算编辑距离
        block = []
        cnt = 0
        for j in range(0, len(a), i):
            if cnt>=num:
                break
            block.append(a[j:j + i])
            cnt += 1
        dis = 0
        pair = itertools.combinations(block,2)
        cnt = 0
        for (j,k) in pair:
            dis += edit_dis(j,k)
            cnt += 1
        dis /= (cnt*i)
        # 记录每次的结果
        record.append({'keysize': i, 'dis': dis})
    # 返回 dis最小的前三位
    return sorted(record, key=lambda c: c['dis'])[0:3]

# 根据 keysize 用单字节攻击爆破，每一位的key
def guess_key(a,keysize):
    key = ''
    for i in range(0,keysize):
        cur =''
        for j in range(0,len(a)):
            if j%keysize ==i:
                cur += a[j]
        key += single_byte_attack(cur)['key']
    return key


def repeating_key_xor(a, key):
    ans = ''
    for i in range(0, len(a)):
        ans += chr(ord(a[i]) ^ ord(key[i % len(key)]))
    return ans


def repeating_key_attack(a):
    keysize = guess_keysize(a)
    record = []
    for ks in keysize:
        key_size = ks['keysize']
        key = guess_key(a,key_size)
        tmp = repeating_key_xor(a,key)
        record.append({'score':calScore(tmp),'ans':tmp})
    return sorted(record,key=lambda c:c['score'])[-1]


file = open('6.txt','r').readlines()
file = ''.join(i.strip() for i in file)
file = decode(file)
# print guess_keysize(file)
print repeating_key_attack(file)['ans']
