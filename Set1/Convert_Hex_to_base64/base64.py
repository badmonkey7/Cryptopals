# coding=utf-8
import sys
def initBase():
    base = []
    # 大写字母
    for i in range(0, 26):
        base.append(chr(i + 65))
    # 小写字母
    for i in range(0, 26):
        base.append(chr(i + 97))
    # 数字
    for i in range(0, 10):
        base.append(chr(i + 48))
    # 其余符号
    base.append('+')
    base.append('/')
    return base


def hex2base64(a):
    base = initBase()
    a = list(a)
    b = []
    # 每24位，即6个hex为一组
    for i in range(0, len(a), 6):
        tmp = bin(int("".join(a[i:i + 6]), 16))[2:]
        # 注意高位要补零
        if len(tmp) % 8 != 0:
            cnt = len(tmp) // 8 + 1
            add = cnt * 8 - len(tmp)
            tmp = '0' * add + tmp
        b.append(tmp)
    ans = ''
    # 将b中元素转化为base64
    for i in range(0, len(b)):
        # b中元素的长度不同，不够的话需要补位
        cur = b[i]
        # 恰好三个字节，不需要补位
        if len(cur) == 24:
            for j in range(0, 24, 6):
                tmp = ("00" + cur[j:j + 6])
                pos = int(tmp, 2)
                ans += base[pos]
        elif len(cur) == 16:
            pos = int(('00' + cur[0:6]), 2)
            ans += base[pos]
            pos = int(('00' + cur[6:12]), 2)
            ans += base[pos]
            pos = int(('00' + cur[12:] + '00'), 2)
            ans += base[pos]
            ans+='='
        elif len(cur) == 8:
            pos = int(('00' + cur[0:6]), 2)
            ans += base[pos]
            pos = int(('00' + cur[6:] + '0000'), 2)
            ans += base[pos]
            ans+="=="
        else:
            print 'error'
            break
    return ans
if __name__=='__main__':
    print hex2base64(sys.argv[1])