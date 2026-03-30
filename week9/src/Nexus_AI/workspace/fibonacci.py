def fibonacci(n: int) -> list:
    """
    Generate the Fibonacci series up to the nth term.

    Args:
    n (int): The number of terms in the Fibonacci series.

    Returns:
    list: A list of integers representing the Fibonacci series.
    """
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


def iterative_fibonacci(n: int, memo: dict = {}) -> int:
    """
    Calculate the nth Fibonacci number using iteration.

    Args:
    n (int): The index of the Fibonacci number to calculate.
    memo (dict, optional): A dictionary to store intermediate results. Defaults to {}.

    Returns:
    int: The nth Fibonacci number.
    """
    if n < 2:
        return n
    elif n in memo:
        return memo[n]
    else:
        result = iterative_fibonacci(n - 1, memo) + iterative_fibonacci(n - 2, memo)
        memo[n] = result
        return result


def recursive_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using recursion.

    Args:
    n (int): The index of the Fibonacci number to calculate.

    Returns:
    int: The nth Fibonacci number.
    """
    if n < 2:
        return n
    else:
        return recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2)