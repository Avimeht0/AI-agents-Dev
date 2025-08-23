""" Factorial
0!=1
1!=1*0!
2!= 2*1!

"""

def Factorial(n):
    if n<2:
        return 1
    return n*Factorial(n-1)
n=int(input("Enter the number: "))
print(f"The factorial of {n} is {Factorial(n)}")