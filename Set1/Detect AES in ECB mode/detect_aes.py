file = open('8.txt','r').readlines()
def detect_aes(target):
    record = []
    for i in range(0,len(target),16):
        record.append(target[i:i+16])
    for item in record:
        if record.count(item)>1:
            return True
    return False
pos = 1
for i in file:
    i = i.strip('\n').decode('hex')
    if detect_aes(i):
        print "Current line is {}   ".format(pos)+'AES_ECB Find!'
    else:
        print "Current line is {}".format(pos)
    pos += 1


