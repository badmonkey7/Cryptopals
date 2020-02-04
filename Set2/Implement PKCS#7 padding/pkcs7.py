def pkcs7padding(target,size):
    tot = len(target)//size
    record = []
    if tot :
        for i in range(0, len(target), size):
            record.append(target[i:i + size])
    pad = tot*size+size-len(target)
    if pad != 0:
        record.append(target[tot*size:]+chr(pad)*pad)
    else:
        record.append(chr(size)*size)
    return ''.join(record)

tar = 'YELLOW SUBMARINE'
size = 20
print pkcs7padding(tar,size)

