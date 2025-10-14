def sortletter(s):
    d = []
    for i in s:
        if i != " ":
            d.append(i)
    c = 0
    while c < len(d):
        for i in range(len(d)-1):
            a = ord(d[i])
            b = ord(d[(i+1)])
            if a > b:
                d[i] , d[i+1] = d[i+1] , d[i]
        c +=1
    print(d)
def sortword(sen):
    l = sen.split(" ")
    for i in range(len(l)-1):
        for j in range(len(l)-1):
            a , b  = ord(l[j][0]) , ord(l[j+1][0])
            if a > b:
                l[j] , l[j+1] = l[j+1] , l[j]
    print(l)
s = input("Enter the str: ")  
sortword(s)
sortletter(s)