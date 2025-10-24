from typing import Generator
import re

def generator_numbers(text:str) -> Generator[float, None, str]:
    """
    Parses string and outputs all found real numbers in "terminating decimals" format, surrounded by whitespaces.

    Parameters:
        text(str): string to parse

    Returns:
        (Generator[float, None, str]): generator object that returns floats one by one 
    """
    current_text = text
    while True:
        # allowing numbers in format 12.34
        match_obj = re.search(r" \d+\.\d+ ",current_text)
        if match_obj:
            current_text = current_text[match_obj.end()+1:]
            # trusting input, not checking for ValueError as indicated in task
            yield float(match_obj.group().strip())
        else:
            return "No more numbers in text"

def sum_profit(text:str, generator_func:Generator[float, None, str]) -> float:
    """
    Sums all provided numbers.

    Parameters:
        text(str): string to parse
        generator_func(Generator[float, None, str]): generator for parsing real numbers from text

    Returns:
        (float): sum of all real numbers found in text    
    """
    result = 0
    for value in generator_func(text):
        result += value
    return result

