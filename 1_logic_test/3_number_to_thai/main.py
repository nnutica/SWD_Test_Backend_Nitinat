"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


DIGITS = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
PLACES = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"]
MAX_NUMBER = 10_000_000


class Solution:

    def number_to_thai(self, number: int) -> str:
        """Convert a number from 0 to 10,000,000 into Thai words."""
        if number < 0:
            return "number can not less than 0"
        if number > MAX_NUMBER:
            return "number can not more than 10000000"
        if number == 0:
            return DIGITS[0]
        return self._read(number)

    def _read(self, number: int) -> str:
        """Read a positive number; the millions part is read by the same rules, then 'ล้าน'."""
        if number >= 1_000_000:
            millions, rest = divmod(number, 1_000_000)
            return self._read(millions) + "ล้าน" + (self._read(rest) if rest else "")

        text = ""
        digits = str(number)
        for position, char in enumerate(digits):
            digit = int(char)
            place = len(digits) - position - 1
            if digit == 0:
                continue
            if place == 1 and digit == 1:
                text += "สิบ"
            elif place == 1 and digit == 2:
                text += "ยี่สิบ"
            # 'เอ็ด' only when a higher digit in this group comes before it: 11, 101 (but 1_000_001 ends in 'หนึ่ง')
            elif place == 0 and digit == 1 and number > 10:
                text += "เอ็ด"
            else:
                text += DIGITS[digit] + PLACES[place]
        return text


if __name__ == "__main__":
    solution = Solution()
    assert solution.number_to_thai(101) == "หนึ่งร้อยเอ็ด"
    assert solution.number_to_thai(-1) == "number can not less than 0"
    assert solution.number_to_thai(0) == "ศูนย์"
    assert solution.number_to_thai(21) == "ยี่สิบเอ็ด"
    assert solution.number_to_thai(1_000_001) == "หนึ่งล้านหนึ่ง"
    assert solution.number_to_thai(10_000_000) == "สิบล้าน"
    assert solution.number_to_thai(10_000_001) == "number can not more than 10000000"
    print("All tests passed")
