# file1=open("myfile.txt",'r')

# reading_file=file1.read()#read the whole data from the file.

# print(reading_file)

# file1.close()

# """method 2 """
# file1=open("myfile.txt",'r')

# reading_file=file1.read(7)#read the 7 char  data from the file.

# print(reading_file)

# file1.close()


# """method 3 """
# file1=open("myfile.txt",'r')

# reading_file=file1.readline()#read the line data from the file.

# print(reading_file)

# file1.close()



with open("myfile.txt",'r') as file2:
    reading_file=file2.read()
    print(reading_file)



with open("myfile.txt",'a') as file2:
    
    file2.write(" There many things you need to learn")
    print(file2.read)
