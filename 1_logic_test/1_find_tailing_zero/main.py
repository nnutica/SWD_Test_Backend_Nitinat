"""
เขียบนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""


class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        """Count trailing zeros of number! without computing the factorial."""
        if number < 0:
            return "number can not be negative"

        # Each zero needs a 2 and a 5; 2s are always more plentiful in n!, so count the 5s.
        # 25, 125, ... carry extra 5s, hence the loop over powers of 5.
        count = 0
        power_of_five = 5
        while power_of_five <= number:
            count += number // power_of_five
            power_of_five *= 5
        return count


if __name__ == "__main__":
    solution = Solution()
    assert solution.find_tailing_zeroes(7) == 1
    assert solution.find_tailing_zeroes(-10) == "number can not be negative"
    assert solution.find_tailing_zeroes(0) == 0
    assert solution.find_tailing_zeroes(25) == 6
    assert solution.find_tailing_zeroes(100_000) == 24_999
    print("All tests passed")
