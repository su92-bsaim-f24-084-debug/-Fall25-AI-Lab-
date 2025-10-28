import math

def mm(crv_d, node, isMax, s, d):
    if crv_d == d:
        return s[node]
    if isMax == True:
        left = mm(crv_d+1, node*2, False, s, d)
        right = mm(crv_d+1, node*2+1, False, s, d)
        return max(left, right)
    else:
        left = mm(crv_d+1, node*2, True, s, d)
        right = mm(crv_d+1, node*2+1, True, s, d)
        return min(left, right)

values = [3, 5, 2, 9, 12, 5, 23, 23]
n = len(values)
treeDepth = int(math.log(n,2))
ans = mm(0,0,True,values,treeDepth)
print("The optimal ans is:", ans)
