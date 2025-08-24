"""Task 2: Write and Append Data to a File
 
Problem Statement: Write a Python program that:
1.   Takes user input and writes it to a file named output.txt.
2.   Appends additional data to the same file.
3.   Reads and displays the final content of the file.
"""

with open("output.txt",'w') as file:
    
    write_file=input("Enter Text to write to the file: ")
    file.write(write_file)


with open("output.txt",'a+') as file:
    
    write_file=input("Enter additional text to append: ")
    file.write('\n'+write_file)


with open("output.txt",'r') as file:
    print(file.read())
