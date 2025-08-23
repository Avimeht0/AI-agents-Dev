"""Task 2: Using the Math Module for Calculations
 
Problem Statement: Write a Python program that:
1.   Asks the user for a number as input.
2.   Uses the math module to calculate the:
o   Square root of the number
o   Natural logarithm (log base e) of the number
o   Sine of the number (in radians)
3.   Displays the calculated results.
"""

import math

# Step 1: Ask the user for a number
try:
    number = float(input("Enter a number: "))

    # Step 2: Perform calculations using the math module
    if number < 0:
        print("Error: Cannot calculate square root or logarithm of a negative number.")
    elif number == 0:
        print("Error: Cannot calculate logarithm of zero.")
    else:
        square_root = math.sqrt(number)
        natural_log = math.log(number)
        sine_value = math.sin(number)

        # Step 3: Display the results
        print(f"Square root: {square_root}")
        print(f"Logarithm: {natural_log}")
        print(f"Sine: {sine_value}")

except ValueError:
    print("Invalid input. Please enter a valid number.")
