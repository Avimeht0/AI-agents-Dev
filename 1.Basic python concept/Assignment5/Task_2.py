"""Task 2: Demonstrate List Slicing 
Problem Statement: Write a Python program that:
1.   Creates a list of numbers from 1 to 10.
2.   Extracts the first five elements from the list.
3.   Reverses these extracted elements.
4.   Prints both the extracted list and the reversed list
"""


numbers=list(range(1,11))

first_five_numbers=numbers[:5]
reverse_first_five_numbers=first_five_numbers[::-1]

print(f"""
Original list: {numbers}
Extracted first five elements: {first_five_numbers}
Reversed extracted elemetns: {reverse_first_five_numbers}""")