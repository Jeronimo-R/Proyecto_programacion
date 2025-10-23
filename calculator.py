c = calculator()
print(c.sum(10,20))
print(c.multiply(10,20))
print(c.divide(10,20))

class calculator:
    def sum(n1,n2):
        return n1+n2
    def multiply(n1,n2):
        return n1*n2
    def divide(n1,n2):
        return n1/n2