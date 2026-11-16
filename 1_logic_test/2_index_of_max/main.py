"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        """Return the index of the largest number, the first one on ties."""
        if not numbers:
            return "list can not blank"

        # Single pass instead of numbers.index(max(numbers)), which walks the list twice
        max_index = 0
        for index in range(1, len(numbers)):
            # Strict '>' keeps the first index when values tie
            if numbers[index] > numbers[max_index]:
                max_index = index
        return max_index


if __name__ == "__main__":
    solution = Solution()
    assert solution.find_max_index([1, 2, 1, 3, 5, 6, 4]) == 5
    assert solution.find_max_index([]) == "list can not blank"
    assert solution.find_max_index([7]) == 0
    assert solution.find_max_index([3, 9, 9]) == 1
    assert solution.find_max_index([-5, -2, -9]) == 1
    print("All tests passed")
