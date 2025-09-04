#!/usr/bin/env python3
"""
Fibonacci Calculator Module

This module provides robust fibonacci number calculation with comprehensive
error handling, input validation, and performance optimization for both
recursive and iterative approaches.

Author: SPARK implementer-spark agent
Date: 2025-09-04
"""

import logging
from typing import Union
import functools


# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FibonacciError(Exception):
    """Custom exception for fibonacci calculation errors."""
    pass


@functools.lru_cache(maxsize=1000)
def fibonacci_recursive(n: int) -> int:
    """
    Calculate fibonacci number using recursive approach with memoization.
    
    This implementation uses functools.lru_cache for memoization to avoid
    redundant calculations and improve performance for repeated calls.
    
    Args:
        n (int): The position in fibonacci sequence (must be >= 0)
        
    Returns:
        int: The fibonacci number at position n
        
    Raises:
        FibonacciError: If n is negative
        TypeError: If n is not an integer
        
    Examples:
        >>> fibonacci_recursive(0)
        0
        >>> fibonacci_recursive(1)  
        1
        >>> fibonacci_recursive(10)
        55
        
    Time Complexity: O(n) with memoization, O(2^n) without
    Space Complexity: O(n) for memoization cache
    """
    # Input validation
    if not isinstance(n, int):
        logger.error(f"Invalid input type: {type(n).__name__}, expected int")
        raise TypeError(f"Expected integer, got {type(n).__name__}")
    
    if n < 0:
        logger.error(f"Negative input not allowed: {n}")
        raise FibonacciError("Fibonacci sequence is not defined for negative numbers")
    
    logger.debug(f"Calculating fibonacci_recursive({n})")
    
    # Base cases
    if n <= 1:
        logger.debug(f"Base case: fibonacci({n}) = {n}")
        return n
    
    # Recursive case with memoization
    result = fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
    logger.debug(f"fibonacci_recursive({n}) = {result}")
    return result


def fibonacci_iterative(n: int) -> int:
    """
    Calculate fibonacci number using iterative approach.
    
    This implementation is memory-efficient and avoids recursion depth limits.
    Recommended for large values of n due to O(1) space complexity.
    
    Args:
        n (int): The position in fibonacci sequence (must be >= 0)
        
    Returns:
        int: The fibonacci number at position n
        
    Raises:
        FibonacciError: If n is negative
        TypeError: If n is not an integer
        
    Examples:
        >>> fibonacci_iterative(0)
        0
        >>> fibonacci_iterative(1)
        1
        >>> fibonacci_iterative(10)
        55
        
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Input validation
    if not isinstance(n, int):
        logger.error(f"Invalid input type: {type(n).__name__}, expected int")
        raise TypeError(f"Expected integer, got {type(n).__name__}")
    
    if n < 0:
        logger.error(f"Negative input not allowed: {n}")
        raise FibonacciError("Fibonacci sequence is not defined for negative numbers")
    
    logger.debug(f"Calculating fibonacci_iterative({n})")
    
    # Handle base cases
    if n <= 1:
        logger.debug(f"Base case: fibonacci({n}) = {n}")
        return n
    
    # Iterative calculation
    prev_prev, prev = 0, 1
    
    for i in range(2, n + 1):
        current = prev_prev + prev
        prev_prev, prev = prev, current
        logger.debug(f"Step {i}: fibonacci({i}) = {current}")
    
    logger.debug(f"fibonacci_iterative({n}) = {prev}")
    return prev


def fibonacci_sequence(count: int) -> list[int]:
    """
    Generate a sequence of fibonacci numbers.
    
    Args:
        count (int): Number of fibonacci numbers to generate (must be >= 0)
        
    Returns:
        list[int]: List containing the first 'count' fibonacci numbers
        
    Raises:
        FibonacciError: If count is negative
        TypeError: If count is not an integer
        
    Examples:
        >>> fibonacci_sequence(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci_sequence(0)
        []
        
    Time Complexity: O(count)
    Space Complexity: O(count)
    """
    # Input validation
    if not isinstance(count, int):
        logger.error(f"Invalid input type: {type(count).__name__}, expected int")
        raise TypeError(f"Expected integer, got {type(count).__name__}")
    
    if count < 0:
        logger.error(f"Negative count not allowed: {count}")
        raise FibonacciError("Count must be non-negative")
    
    logger.info(f"Generating fibonacci sequence of length {count}")
    
    if count == 0:
        return []
    
    sequence = [0]
    if count == 1:
        return sequence
    
    sequence.append(1)
    
    for i in range(2, count):
        next_fib = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_fib)
        logger.debug(f"Added fibonacci({i}) = {next_fib}")
    
    logger.info(f"Generated sequence: {sequence}")
    return sequence


def fibonacci(n: int, method: str = "iterative") -> int:
    """
    Calculate fibonacci number using specified method.
    
    This is the main public interface that provides a choice between
    recursive and iterative implementations.
    
    Args:
        n (int): The position in fibonacci sequence (must be >= 0)
        method (str): Calculation method, either "iterative" or "recursive"
        
    Returns:
        int: The fibonacci number at position n
        
    Raises:
        FibonacciError: If n is negative or method is invalid
        TypeError: If n is not an integer
        
    Examples:
        >>> fibonacci(10)
        55
        >>> fibonacci(10, method="recursive")
        55
        >>> fibonacci(0)
        0
        
    Note:
        For large values of n (> 30), iterative method is recommended
        for better performance and to avoid recursion depth limits.
    """
    # Validate method parameter
    valid_methods = {"iterative", "recursive"}
    if method not in valid_methods:
        logger.error(f"Invalid method: {method}")
        raise FibonacciError(f"Method must be one of {valid_methods}")
    
    logger.info(f"Calculating fibonacci({n}) using {method} method")
    
    try:
        if method == "recursive":
            result = fibonacci_recursive(n)
        else:  # iterative
            result = fibonacci_iterative(n)
        
        logger.info(f"Successfully calculated fibonacci({n}) = {result}")
        return result
        
    except (TypeError, FibonacciError) as e:
        logger.error(f"Fibonacci calculation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in fibonacci calculation: {e}")
        raise FibonacciError(f"Calculation failed due to unexpected error: {e}")


def is_fibonacci_number(num: Union[int, float]) -> bool:
    """
    Check if a number is a fibonacci number.
    
    Uses the mathematical property that a number n is fibonacci if
    one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square.
    
    Args:
        num (Union[int, float]): Number to check
        
    Returns:
        bool: True if the number is a fibonacci number, False otherwise
        
    Examples:
        >>> is_fibonacci_number(0)
        True
        >>> is_fibonacci_number(1)
        True
        >>> is_fibonacci_number(4)
        False
        >>> is_fibonacci_number(5)
        True
    """
    if not isinstance(num, (int, float)):
        return False
    
    if num < 0 or num != int(num):
        return False
    
    num = int(num)
    
    def is_perfect_square(n: int) -> bool:
        if n < 0:
            return False
        root = int(n ** 0.5)
        return root * root == n
    
    # A number is fibonacci if one of these is a perfect square
    return (is_perfect_square(5 * num * num + 4) or 
            is_perfect_square(5 * num * num - 4))


def main():
    """
    Demonstration of fibonacci calculator functionality.
    
    This function shows various usage examples and error handling scenarios.
    """
    print("=== Fibonacci Calculator Demo ===\n")
    
    # Basic calculations
    print("1. Basic fibonacci calculations:")
    test_values = [0, 1, 5, 10, 20]
    for n in test_values:
        try:
            result = fibonacci(n)
            print(f"   fibonacci({n}) = {result}")
        except Exception as e:
            print(f"   Error calculating fibonacci({n}): {e}")
    
    print("\n2. Fibonacci sequence generation:")
    try:
        sequence = fibonacci_sequence(10)
        print(f"   First 10 fibonacci numbers: {sequence}")
    except Exception as e:
        print(f"   Error generating sequence: {e}")
    
    print("\n3. Method comparison (recursive vs iterative):")
    n = 15
    try:
        recursive_result = fibonacci(n, method="recursive")
        iterative_result = fibonacci(n, method="iterative")
        print(f"   fibonacci({n}) recursive: {recursive_result}")
        print(f"   fibonacci({n}) iterative: {iterative_result}")
        print(f"   Results match: {recursive_result == iterative_result}")
    except Exception as e:
        print(f"   Error in method comparison: {e}")
    
    print("\n4. Fibonacci number validation:")
    test_numbers = [0, 1, 2, 3, 4, 5, 8, 13, 21, 22]
    for num in test_numbers:
        is_fib = is_fibonacci_number(num)
        print(f"   Is {num} a fibonacci number? {is_fib}")
    
    print("\n5. Error handling demonstration:")
    error_cases = [
        (-1, "Negative number"),
        ("10", "String input"),
        (10.5, "Float input for main fibonacci function")
    ]
    
    for test_input, description in error_cases:
        try:
            result = fibonacci(test_input)
            print(f"   {description}: {result} (unexpected success)")
        except Exception as e:
            print(f"   {description}: Properly caught error - {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Enable debug logging for demonstration
    logging.getLogger().setLevel(logging.DEBUG)
    main()