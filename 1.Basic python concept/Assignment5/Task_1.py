"""Task 1: Create a Dictionary of Student Marks

Problem Statement: Write a Python program that:
1.   Creates a dictionary where student names are keys and their marks are values.
2.   Asks the user to input a student's name.
3.   Retrieves and displays the corresponding marks.
4.   If the student’s name is not found, display an appropriate message."""

students={
    "Arvind":90,
    "Ravi":78,
    "Rajesh":79,
    "Upendar":100,
    "RK":40
}
Name=input("Enter the student's name : ")

if Name in students.keys():
    print(f"{Name}'s marks {students[Name]}.")
else:
    print("Student not found.")