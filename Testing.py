# Algortithm of Count()
# Initialize an accumulator (count)
# loop through list with for-loop
# if i == x(what we want to count), update count
# else, leave count
# print count
def Count(lst, x):
    count = 0
    for i in lst:
        if i == x:
            count = count + 1
        else:
            count = count
    print("The number of instances of", "'" + x + "'" + " " + "is", count)


# Algorithm for isin()
# initialize accumulator (count)
# loop through list with for-loop
# if i == x(what we want to keep count of), update count. Else leave count
# if count greater than 0, print True, else print False
def isin(mlst, x):
    count = 0
    for i in mlst:
        if i == x:
            count = count + 1
        else:
            count = count
    if count > 0:
        print("True")
    else:
        print("False")


# Algorithm of reverse()
# Use slice method starting from last item in list (list[-1]) and reverse by using stepsize that goes back by 1 (-1)
# print list
def Reverse(slst):
    a = slst[-1::-1]
    print("The reverse list is: ", a)


# Algorithm of index
# Compare each item in list with for-loop ranging by length of list
# compare each item  using if-statement
# once list[i] == x, print i
def index(mylist, x):
    for i in range(len(mylist)):
        if mylist[i] == x:
            print("Index of", x + " is", i)
            break


# Algorith for sort
# Use for-loop ranging from index 1 to last item in list
# create variable that holds value of indices that are looped through (lst)
# create another variable that will be sentinel (i)
# compare items in list using lst and i  and if-else statement and then updating lst
def sort(mylst):
    for x in range(1, len(mylst)):
        lst = mylst[x]
        i = x - 1
        while i >= 0:
            if lst < mylst[i]:
                mylst[i + 1] = mylst[i]
                mylst[i] = lst
                i = i - 1
            else:
                break


def main():
    n = input("Input a list of items seperated commas (,): ")
    lstt = n.split(", ")
    s = input("What item do you want to count the number of instances in this list?: ")
    Count(lstt, s)
    Reverse(lstt)
    index(lstt, s)
    sort(lstt)


main()


