def fast_fibonacci(n: int) -> int:
    """
    Compute the nth Fibonacci number using the fast doubling method.
    
    Time Complexity: O(log n)
    Space Complexity: O(log n) due to recursion stack

    Parameters:
    ----------
    n : int
        The position in the Fibonacci sequence to compute. Must be non-negative.

    Returns:
    -------
    int
        The nth Fibonacci number.
    """

    def fib_helper(k: int) -> tuple[int, int]:
        """
        Helper function that returns a tuple (F(k), F(k+1)) using fast doubling.
        
        Parameters:
        ----------
        k : int
            The index of the Fibonacci number.
        
        Returns:
        -------
        tuple[int, int]
            A tuple containing (F(k), F(k+1)).
        """
        if k == 0:
            return (0, 1)

        # Recursive call
        a, b = fib_helper(k // 2)

        # Apply the fast doubling formulas
        c = a * (2 * b - a)           # F(2k) = F(k) * [2F(k+1) - F(k)]
        d = a * a + b * b             # F(2k+1) = F(k)^2 + F(k+1)^2

        if k % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)         # Shifted for F(k+1) and F(k+2)

    # Only return the first value: F(n)
    return fib_helper(n)[0]

# Example usage:
if __name__ == "__main__":
    n = 10
    print(f"The {n}th Fibonacci number is {fast_fibonacci(n)}")
