import string

file = open('english.txt', 'r').readlines()
cnt = 0
cntApp = [0 for i in range(0, 27)]
for i in file:
    for j in i:
        if j == ' ':
            cntApp[26] += 1
            cnt += 1
        elif j in string.ascii_letters:
            cntApp[ord(j.lower()) - 97] += 1
            cnt += 1
alpha = []
for i in range(0, 26):
    alpha.append(chr(i + 97))
All = alpha + [' ']
for i in range(0, len(cntApp)):
    cntApp[i] = cntApp[i] * 1.0 / cnt
point = {i: j for i, j in zip(All, cntApp)}
print point
