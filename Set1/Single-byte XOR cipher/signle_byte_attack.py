# coding=utf-8
import  string
# point = { #字符频率表
#     'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
#     'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
#     'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
#     'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}
point = {' ': 0.19742661841576195, 'a': 0.06420816818886782, 'c': 0.01653167901660061, 'b': 0.011281521052329255, 'e': 0.10504911252800275, 'd': 0.03145499454305244, 'g': 0.0146705726922856, 'f': 0.015624102475730943, 'i': 0.057671319432477455, 'h': 0.05185823424665403, 'k': 0.006904474696995806, 'j': 0.0008731116089379057, 'm': 0.021092538342236775, 'l': 0.03654431615830892, 'o': 0.060095352978344535, 'n': 0.052099488770176346, 'q': 0.0008156700557183066, 'p': 0.013866390947211213, 's': 0.049135504624045034, 'r': 0.043655580446895284, 'u': 0.022057556436326037, 't': 0.08013096674134068, 'w': 0.01880636452409673, 'v': 0.007777586305933713, 'y': 0.01828939054512034, 'x': 0.0017232465965879718, 'z': 0.0003561376299615142}
def calScore(a):
    sc = 0
    for i in a:
        if i in point:
            sc+=point[i]
    return  sc
# target 是纯字符没有经过任何的编码
def signle_byte_attack(target):
    key = 0
    ans = ''
    mx = 0
    for i in range(0, 256):
        flag = ''
        if len(target)%2 != 0:
            return {'ans':'','key':'','score':0}
        for j in range(0, len(target), 2):
            tmp = target[j:j + 2]
            flag += chr(i^ord(tmp[0]))
            flag += chr(i^ord(tmp[1]))
        if mx<calScore(flag):
            mx = calScore(flag)
            ans =flag
            key = chr(i)
    return {'ans':ans,'key':key,'score':mx}

target = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
print signle_byte_attack(target.decode('hex'))