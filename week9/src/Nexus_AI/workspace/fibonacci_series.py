import sys

def get_input_from_user():
    while True:
        try:
            n = int(input("Enter the number of terms in the Fibonacci series: " ))
            if n < 1:
                print("Error: Input must be a positive integer.")
                continue
            return n
        except ValueError:
            print("Error: Input must be a positive integer.")

def generate_fibonacci_series(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        series = [0, 1]
        for _ in range(2, n):
            series.append(series[-1] + series[-2])
        return series

def print_result(result):
    if isinstance(result, list):
        print("Fibonacci series:", result)
    else:
        print(result)

n = get_input_from_user()
result = generate_fibonacci_series(n)
print_result(result)

