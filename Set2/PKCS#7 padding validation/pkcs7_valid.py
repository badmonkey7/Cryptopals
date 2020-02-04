def pkcs7_valid(s):
    lenghth = len(s)
    tag = s[-ord(s[-1])]
    for i in range(ord(s[-1]),0,-1):
        if  tag != s[i]:
            print 'Invalid padding String is given,Please check your string!'
            return False
    res = s[0:-ord(s[-1])]
    if len(res)+ord(s[-1]) == lenghth:
        print res
        return True
    else:
        print 'Invalid padding String is given,Please check your string!'
        return False

pkcs7_valid("ICE ICE BABY\x01\x02\x03\x04")