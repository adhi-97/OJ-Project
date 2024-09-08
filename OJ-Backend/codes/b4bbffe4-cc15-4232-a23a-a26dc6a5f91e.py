# Function to add two numbers
def add_two_numbers(num1, num2):
    return num1 + num2

# Input: two numbers
number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))

# Calculate the sum
sum_result = add_two_numbers(number1, number2)

# Output: display the result
print(f"The sum of {number1} and {number2} is {sum_result}.")
