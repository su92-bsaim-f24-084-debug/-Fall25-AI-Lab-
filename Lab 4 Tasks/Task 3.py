c_n = '4214618100583692'
l_n = int(c_n[-1])
c_n = c_n[:-1]
c_n = c_n [::-1]
l =[]
a = 0
for i in c_n:
    l.append(int(i))
print(l)
for i in range(len(l)):
    if i % 2 == 0:
        l[i] *= 2
        if l[i] > 9:
            l[i] -= 9
    a += l[i]
a += l_n
if a % 10 == 0:
    print("Card is valid")
else:
    print("Invalid card") 
