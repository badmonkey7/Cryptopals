def encry(mess, key):
    res = ''
    length = len(key)
    for i in range(0, len(mess)):
        tmp = ord(mess[i]) ^ ord(key[i % length])
        tmp = "{:02x}".format(tmp)
        res += tmp
    return res
mess = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = 'ICE'
print encry(mess,key)
code = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
print code