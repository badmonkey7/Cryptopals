from MT19937 import  MT19937
from time import time
from random import randint

curTime = int(time())
add = randint(40,100)
seed = curTime+add
print 'set seed {}'.format(seed)
prng = next(MT19937(seed).random_32())
add2 = randint(40,100)
now = curTime+add+add2
def crack_seed(now,prng):
    guess = next(MT19937(now).random_32())
    while guess!=prng:
        now -= 1
        guess = next(MT19937(now).random_32())
    print 'The seed is {}'.format(now)
    return now
crack_seed(now,prng)