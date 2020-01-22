# coding=utf-8
file = open('4.txt', 'r').readlines()
# print file
point = {'e': 0.1202, 't': 0.0910, 'a': 0.0812, 'o': 0.0768, 'i': 0.0731,
         'n': 0.0695, 's': 0.0628, 'r': 0.0602, 'h': 0.0592, 'd': 0.0432,
         'l': 0.0398, 'u': 0.0288, 'c': 0.0271, 'm': 0.0261, 'f': 0.0230,
         'y': 0.0211, 'w': 0.0209, 'g': 0.0203, 'p': 0.0182, 'b': 0.0149,
         'v': 0.0111, 'k': 0.0069, 'x': 0.0017, 'q': 0.0011, 'j': 0.0010, 'z': 0.0007}
# point = { #字符频率表
#     'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
#     'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
#     'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
#     'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}

def calScore(a):
    score = 0
    for i in a:
        i = i.lower()
        if i in point:
            score += point[i]
    return score


# target 为一个字符串
def single_byte_attack(target):
    ans = ''
    mx = 0
    key = ''
    for i in range(0, 256):
        flag = ''
        if len(target)%2 != 0:
            return {'ans':'','key':'','score':0}
        for j in range(0, len(target), 2):
            tmp = target[j:j + 2]
            flag += chr(i ^ ord(tmp[0]))
            flag += chr(i ^ ord(tmp[1]))
        if mx < calScore(flag):
            mx = calScore(flag)
            ans = flag
            key = chr(i)
    return {'ans':ans,'key':key,'score':mx}


ans = ''
sc = 0
for i in file:
    i = i.strip('\n').decode('hex')
    cur = single_byte_attack(i)
    if cur['score']>sc:
        sc = cur['score']
        ans = cur['ans']
print ans,sc


