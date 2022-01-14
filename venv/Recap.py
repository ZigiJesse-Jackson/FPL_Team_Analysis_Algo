import re

def student_discount(x):
    return 0.9*x

def reg_buyer(x):
    return 0.95*x

#Using functional programming
#print(reg_buyer(student_discount(14)))

#using lambda expression
#print((lambda x: x*(x+5)**2)(5))

#Using maps to perform operations
prices = [20, 55, 12, 12, 34,34,45,26,57,35,45]
discounted_prices = list(map(student_discount, prices))
#print(discounted_prices)

#Inheritance practice
class Computer:
    specs = ""

    def __init__(self, specs):
        self.specs = specs

    def get_specs(self):
        return specs

    def display_specs(self):
        print("Specs:{0}".format(self.specs))



class Laptop(Computer):
    def get_specs(self):
        return self.specs

    def display_specs(self):
        print("Laptop specs: {0}".format(self.specs))


class Desktop(Computer):
    def get_specs(self):
        return self.specs

    def display_specs(self):
        print("Desktop specs: {0}".format(self.specs))


laptop = Laptop("3GB Ram")
#laptop.display_specs()

#operation overloading
#overloaded multiplication for Overload class
class Overload:

    def __init__(self, x):
        self.x = x


    def __mul__(self, other):
        return self.x + other.x


wpa = Overload(5)

ohk = Overload(4)

#print(wpa * ohk)


pattern = r"[A-Za-z0-9][A-Za-z].[A-Za-z]"

if re.search(pattern, "3r2y"):
    print("Match")
