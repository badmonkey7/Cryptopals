from base64 import b64decode
from Crypto.Cipher import AES
import os
f = open('20.txt','r').readlines()
#
key = os.urandom(16)
nonce = chr(0)*8
#
xor = lambda a,b:''.join([chr(ord(a[i])^ord(b[i])) for i in range(min(len(a),len(b)))])
#
def CTR(m):
    cipher = AES.new(key,AES.MODE_ECB)
    bs = AES.block_size
    stream = ''
    for i in range(len(m)/bs+1):
        stream += cipher.encrypt(nonce+chr(i)+chr(0)*7)
    return xor(stream,m)
#
point = {' ': 0.19742661841576195, 'a': 0.06420816818886782, 'c': 0.01653167901660061, 'b': 0.011281521052329255,
         'e': 0.10504911252800275, 'd': 0.03145499454305244, 'g': 0.0146705726922856, 'f': 0.015624102475730943,
         'i': 0.057671319432477455, 'h': 0.05185823424665403, 'k': 0.006904474696995806, 'j': 0.0008731116089379057,
         'm': 0.021092538342236775, 'l': 0.03654431615830892, 'o': 0.060095352978344535, 'n': 0.052099488770176346,
         'q': 0.0008156700557183066, 'p': 0.013866390947211213, 's': 0.049135504624045034, 'r': 0.043655580446895284,
         'u': 0.022057556436326037, 't': 0.08013096674134068, 'w': 0.01880636452409673, 'v': 0.007777586305933713,
         'y': 0.01828939054512034, 'x': 0.0017232465965879718, 'z': 0.0003561376299615142}
# point =  {
#     'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
#     'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
#     'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
#     'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
# }
def calScore(a):
    res = 0
    for i in a:
        try:
            i = i.lower()
        except:
            pass
        if point.has_key(i):
            res += point[i]
    return res

def guess_key(enc):
    mx = 0
    key = ''
    for i in range(256):
        tmp = ''.join([chr(ord(j)^i) for j in enc])
        sc = calScore(tmp)
        if sc>mx:
            key = chr(i)
            mx = sc
    return key
#
def fix_nonce_attack():
    enc = [CTR(b64decode(i.strip('\n'))) for i in f]
    key = ''
    for i in range(max(map(len,enc))):
        cur = []
        for j in enc:
            try:
                cur.append(j[i])
            except:
                pass
        key += guess_key(''.join(cur))
    for i in enc:
        print xor(key,i)
    # return ''.join([xor(key,i) for i in enc])





fix_nonce_attack()

