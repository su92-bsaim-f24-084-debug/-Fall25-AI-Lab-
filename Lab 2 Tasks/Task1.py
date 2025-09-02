import random as r 
print("If it is neither Fizz nor Buzz,then only press enter(dont pass any value).")
n2 = 0
s = 0
while True:
    n1 = r.randint(1,100)
    print("The number is: ",n1)
    i = input("Enter : ")
    i = i.lower()
    i = i.replace(" ","")
    c1 = (n1+n2) % 3 == 0
    c2 = (n1+n2) %5 == 0
    c3 = (n1+n2) % 5 == 0 and  (n1+n2) % 3 == 0
    if c3:
        if c3 and i == "fizzbuzz":
            s+=1
            print("You are doing great")
        else:
            print("Wrong answer!!! You lose\nYour score is ",s)
            exit()
    elif c1 or c2:
        if c2 and i == "buzz":
            s+=1
            print('You are doing great')
        elif c1 and i == "fizz":
            s+=1
            print("You are doing great")
        else:
            print("Wrong answer!!! You lose\nYour score is ",s)
            exit()
    elif i == "":
            print("You are doing great")
    elif i:
        exit("Wrong answer!!! You lose\nYour score is",s)
    n2 = n1       
