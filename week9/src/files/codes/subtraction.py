# subtraction.py

def subtract(num1, num2):
    """
    This function subtracts two numbers.

    Args:
        num1 (float): The first number.
        num2 (float): The second number.

    Returns:
        float: The result of the subtraction.
    """
    return num1 - num2

def main():
    # Example usage:
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    result = subtract(num1, num2)
    print(f"The result of {num1} - {num2} is {result}")

if __name__ == "__main__":
    main()