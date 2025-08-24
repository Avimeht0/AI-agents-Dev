"""Task 1: Read a File and Handle Errors 
Problem Statement:  Write a Python program that:
1.   Opens and reads a text file named sample.txt.
2.   Prints its content line by line.
3.   Handles errors gracefully if the file does not exist.
"""

try:
    with open("simple.txt",'r+') as file:
        i=1
        for line in file:
            print(f"line {i}: ",line.strip())
            i+=1
except:
    print("Error: The file 'simple.txt' was not found.")
