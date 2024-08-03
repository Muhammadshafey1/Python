def factorial(n):
    # Base case: factorial of 0 or 1 is 1
    if n == 0 or n == 1:
        return 1
    else:
        # Recursive case: n! = n * (n-1)!
        return n * factorial(n - 1)

# Get user input
n = int(input("Enter a non-negative integer to calculate its factorial: "))

# Validate input
if n < 0:
    print("Error: Factorial is not defined for negative numbers.")
else:
    # Calculate factorial
    result = factorial(n)
    
    # Display the result
    print(f"The factorial of {n} is {result}")
    
    
    
