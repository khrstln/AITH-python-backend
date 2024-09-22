import math
from typing import List


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")

    return math.factorial(n)


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return b


def mean(nums: List[int] | List[float]) -> float:
    if not nums:
        raise ValueError("list must be non-empty")

    return sum(nums) / len(nums)
