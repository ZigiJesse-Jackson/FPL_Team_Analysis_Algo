def recReverse(i, n, list):
    if n - i == 2:
        return list
    if n - i < 0:
        return list

    list[i], list[n] = list[n], list[i]
    i += 1
    n -= 1
    return recReverse(i, n, list)

def hehe():
    i =0
    j = 23
    return i,j
m=hehe()
print(m)