""" Method 1 To open a file """


file1=open("myfile.txt",'r')
"""here the in open first part is the provide the directory of the file and
 second one is mode at what mode you want to open the file read (r), write (w) """

#in this we need to close the file 

file1.close()
""" Method 2 """

with open("myfile.txt",'w') as file1:
    None