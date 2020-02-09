# coding=utf-8
# 参考wiki
# https://en.m.wikipedia.org/wiki/Mersenne_Twister
# https://cedricvanrompay.gitlab.io/cryptopals/challenges/21.html
# https://zh.wikipedia.org/wiki/%E6%A2%85%E6%A3%AE%E6%97%8B%E8%BD%AC%E7%AE%97%E6%B3%95
class MT19937():
    def __init__(self,seed):
        self.pos = 0
        self.x = list()
        self.x.append(seed)
    # 32 位标准
    def random_32(self):
        # 32位随机数的参数
        (w, n, m, r, a) = (32, 624, 397, 31, 0x9908B0DF)
        (u, d) = (11, 0xFFFFFFFF)
        (s, b) = (7, 0x9D2C5680)
        (t, c) = (15, 0xEFC60000)
        l = 18
        f = 1812433253
        # 初始化
        for i in range(1, n):
            tmp = (f * (self.x[i - 1] ^ (self.x[i - 1] >> (w - 2))) + i) & d
            self.x.append(tmp)
        upper_mask = d << r & d
        lower_mask = d >> (w - r) & d
        # 旋转
        for i in range(n):
            tmp = ((self.x[i] & upper_mask) + (self.x[(i + 1) % n] & lower_mask)) & d
            if tmp & 1:
                tmp = tmp >> 1 ^ a
            else:
                tmp >>= 1
            tmp ^= self.x[(i + m) % n]
            self.x[i] = tmp
        # 提取
        while True:
            y = self.x[self.pos]
            y = y ^ y >> u
            y = y ^ y << s & b
            y = y ^ y << t & c
            y = y ^ y >> l
            self.pos = (self.pos + 1) % n
            # 使用generator
            yield y & d

    # 64 位标准
    def random_64(self):
        # 32位随机数的参数
        (w, n, m, r, a) = (64, 312, 156, 31, 0xB5026F5AA96619E9)
        (u, d) = (29, 0x5555555555555555)
        (s, b) = (17, 0x71D67FFFEDA60000)
        (t, c) = (37, 0xFFF7EEE000000000)
        l = 43
        f = 6364136223846793005
        # 初始化
        for i in range(1, n):
            tmp = (f * (self.x[i - 1] ^ (self.x[i - 1] >> (w - 2))) + i) & d
            self.x.append(tmp)
        upper_mask = d << r & d
        lower_mask = d >> (w - r)
        # 旋转
        for i in range(n):
            tmp = (self.x[i] & upper_mask) + (self.x[(i + 1) % n] & lower_mask)
            if tmp & 1:
                tmp = tmp >> 1 ^ a
            else:
                tmp >>= 1
            tmp ^= self.x[(i + m) % n]
            self.x[i] = tmp
            # 提取
            while True:
                y = self.x[self.pos]
                y = y ^ y >> u
                y = y ^ y << s & b
                y = y ^ y << t & c
                y = y ^ y >> l
                self.pos = (self.pos + 1) % n
                # 使用generator
                yield y & d






