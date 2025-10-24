from typing import Callable

def caching_fibonacci() -> Callable[[int],int]:
    """
    Generates function object to count n-th Fibonacci number with caching optimisation.

    Returns:
       Callable[[int],int]: function to count fibonacci numbers with internal cache using closure.
    """
    # recursion base cases are already in cache
    cache = {0:0, 1:1}

    def fibonacci(n:int) -> int:
        """
        Returns n-th Fibonacci number. Uses recursion and caching as an optimisation.

        Formulars for positive and negative Fibonacci numbers can be found here: https://en.wikipedia.org/wiki/Fibonacci_sequence

        Parameters:
            n(int): sequential number of required Fibonacci number, can be both negative and positive.

        Returns:
            (int): corresponding value of Fibonacci number.

        """
        if n < 0:
            # to effectively use cache let's calculate negative index number using positive index one
            return ((-1)**(n%2))*fibonacci(-n)
        if n not in cache:
            # to overcome recursion limit when working with n>1000 let's warm cache
            list(map(fibonacci,range(1000,n,1000)))
            cache[n] = fibonacci(n-2) + fibonacci(n-1)    
        return cache[n]
    
    return fibonacci
