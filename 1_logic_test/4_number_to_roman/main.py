"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


# Subtractive pairs (CM, CD, ...) are in the table, so the greedy loop needs no special cases
ROMAN_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]
MAX_NUMBER = 3999


class Solution:

    def number_to_roman(self, number: int) -> str:
        """Convert a number from 1 to 3999 into a Roman numeral."""
        if number < 0:
            return "number can not less than 0"
        # Roman numerals have no zero
        if number == 0:
            return "number can not be 0"
        # Standard notation tops out at MMMCMXCIX
        if number > MAX_NUMBER:
            return "number can not more than 3999"

        roman = ""
        for value, symbol in ROMAN_VALUES:
            count, number = divmod(number, value)
            roman += symbol * count
        return roman


if __name__ == "__main__":
    solution = Solution()
    assert solution.number_to_roman(101) == "CI"
    assert solution.number_to_roman(-1) == "number can not less than 0"
    assert solution.number_to_roman(0) == "number can not be 0"
    assert solution.number_to_roman(1994) == "MCMXCIV"
    assert solution.number_to_roman(3999) == "MMMCMXCIX"
    assert solution.number_to_roman(4000) == "number can not more than 3999"
    print("All tests passed")
