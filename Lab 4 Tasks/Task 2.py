sen = 'I am Abdul-Rehman'
l = sen.split(" ")
for i in range(len(l)-1):
    for j in range(len(l)-1):
        a , b  = ord(l[j][0]) , ord(l[j+1][0])
        if a > b:
            l[j] , l[j+1] = l[j+1] , l[j]
print(l)
