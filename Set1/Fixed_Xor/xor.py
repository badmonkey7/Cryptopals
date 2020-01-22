def xor(a,b):
    a=int(a,16)
    b=int(b,16)
    print hex(a^b)[2:].strip('L')
a = '1c0111001f010100061a024b53535009181c'
b = '686974207468652062756c6c277320657965'
xor(a,b)