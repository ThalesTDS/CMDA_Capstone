# This module provides basic arithmetic operations through functions and a Calculator class.

def add(a: float, b: float) -> float:
    """
    Adds two numbers and returns the result.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b

class Calculator:
    """
    A simple calculator class for performing basic arithmetic operations.

    Methods:
        multiply(a, b): Multiplies two numbers and returns the result.
    """

    def multiply(self, a: float, b: float) -> float:
        """
        Multiplies two numbers and returns the result.

        Parameters:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of the two numbers.
        """
        return a * b
