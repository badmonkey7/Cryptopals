# coding=utf-8
from MT19937 import MT19937
# invert right
def invert_right(m,l,val=''):
    length = 32
    mx = 0xffffffff
    if val == '':
        val = mx
    i,res = 0,0
    while i*l<length:
        mask = (mx<<(length-l)&mx)>>i*l
        tmp = m & mask
        m = m^tmp>>l&val
        res += tmp
        i += 1
    return res
# invert left
def invert_left(m,l,val):
    length = 32
    mx = 0xffffffff
    i,res = 0,0
    while i*l < length:
        mask = (mx>>(length-l)&mx)<<i*l
        tmp = m & mask
        m ^= tmp<<l&val
        res |= tmp
        i += 1
    return res

# invert temper
def invert_temper(m):
    m = invert_right(m,18)
    m = invert_left(m,15,4022730752)
    m = invert_left(m,7,2636928640)
    m = invert_right(m,11)
    return m
# 注意事项: temper 可以破解是因为可以对位移进行求逆，但是并不是所有的位移都可以求逆，
# 对一个数 进行 m = m^m>>c&d 是不会改变 m的位数的 即右移运算不改变位数
# 但是如果进行左移运算是可能改变位数的，如果位数一旦改变，就无法确定，求逆过程中循环的次数
# 特殊的是，我们知道 MT算法中的 state 元素都是 32位的，所以可以求逆
def clone_mt(prng):
    record = []
    for _ in range(624):
        record.append(next(prng))
    state = [invert_temper(i) for i in record]
    pos = 0
    while True:
        y = state[pos]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        pos = (pos+1)%624
        yield y & 0xffffffff
prng = MT19937(8888).random_32()
myprng = clone_mt(prng)
prng = MT19937(8888).random_32()
for i in range(1000):
    if next(prng) != next(myprng):
        print '第{}个随机数不相等'.format(i)
        break
