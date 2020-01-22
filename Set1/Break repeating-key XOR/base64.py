# coding=utf-8
def initBase():
    base = []
    for i in range(0, 26):
        base.append(chr(ord('A') + i))
    for i in range(0, 26):
        base.append(chr(ord('a') + i))
    for i in range(0, 10):
        base.append(chr(ord('0') + i))
    base.append('+')
    base.append('/')
    return base


def encode(a):
    base = initBase()
    Len = len(a) // 3
    ans = ''
    # 处理正常的三位
    for i in range(0, Len):
        st = i * Len
        cur = a[st:st + 3]
        tmp = ''
        for j in cur:
            tmp += "{:08b}".format(ord(j))
        for i in range(0, len(tmp), 6):
            ans += base[int("00" + tmp[i:i + 6], 2)]
    Left = len(a) - Len * 3
    if Left == 1:
        cur = a[3 * Len:]
        tmp = ''
        for i in cur:
            tmp += "{:08b}".format(ord(i))
        ans += base[int(("00" + tmp[0:6]), 2)]
        ans += base[int(("00" + tmp[6:] + "0000"), 2)]
        ans += "=="
    elif Left == 2:
        cur = a[3 * Len:]
        tmp = ''
        for i in cur:
            tmp += "{:08b}".format(ord(i))
        ans += base[int(("00" + tmp[0:6]), 2)]
        ans += base[int(("00" + tmp[6:12]), 2)]
        ans += base[int(("00" + tmp[12:] + "00"), 2)]
        ans += '='
    return ans


def decode(a, pattern='hex'):
    pos = [i for i in range(0, 64)]
    base = initBase()
    Map = {i: j for i, j in zip(base, pos)}
    # Map = dict(zip(base,pos))
    ans = ''
    # 解码的时候每四位处理
    if len(a) % 4 != 0:
        print 'error length'
        exit(0)
    for i in range(0, len(a), 4):
        # 特殊处理填充位
        cur = a[i:i + 4]
        if cur[3] == '=' and cur[2] == '=':
            cal = ''
            tmp = '{:08b}'.format(Map[cur[0]])[2:]
            cal += tmp
            tmp = '{:08b}'.format(Map[cur[1]])[2:4]
            cal += tmp
            if pattern == 'hex':
                ans += "{:02x}".format(int(cal, 2)).decode('hex')
            elif pattern == 'bin':
                ans += tmp
        elif cur[3] == '=' and cur[2] != '=':
            cal = ''
            cal += '{:08b}'.format(Map[cur[0]])[2:]
            cal += '{:08b}'.format(Map[cur[1]])[2:]
            cal += '{:08b}'.format(Map[cur[2]])[2:6]
            if pattern == 'hex':
                ans += "{:04x}".format(int(cal, 2)).decode('hex')
            elif pattern == 'bin':
                ans += tmp
        else:
            cal = ''
            for j in cur:
                tmp = "{:08b}".format(Map[j])[2:]
                cal += tmp
            if pattern == 'hex':
                ans += "{:06x}".format(int(cal, 2)).decode('hex')
            elif pattern == 'bin':
                ans += tmp
    return ans
