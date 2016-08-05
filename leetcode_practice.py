import math


class Solution(object):
    """
    exercises on LeetCode
    """

    def __init__(self):
        pass

    def reverse_words(self):
        """
        reverse a string word by word.
        :return: Str
        """
        my_string = raw_input("Enter a string:")
        ret = " ".join(my_string.split()[::-1])
        return ret

    def is_palindrome(self, s):
        """
        determine if the given string is a palindrome, considering only alphanumeric characters and ignoring cases.
        :param s: Str
        :return: Bool
        """
        my_string = "".join(ch for ch in str(s) if ch.isalnum())
        test_string = my_string.lower()
        if len(test_string) <= 0:
            return True
        else:
            return test_string[0] == test_string[-1] and Solution().is_palindrome(test_string[1:-1])

    def is_palindrome2(self, s):
        """
        another solution to isPalindrome().
        """
        my_string = "".join(ch for ch in str(s) if ch.isalnum())
        reversed_string = my_string[::-1]
        return my_string == reversed_string

    def two_sum(self, nums, target):
        """
        return indices of the 2 numbers in the given list such that they add up to the target.
        :param nums: List[int]
        :param target: int
        :return: (index1, index2)
        """
        length = len(nums)
        for i in range(length):
            for j in range(i + 1, length):
                if nums[i] + nums[j] == target:
                    return i, j
        return None

    def two_sum2(self, nums, target):
        """
        Solution2 to twoSum() using hash method.
        """
        nums_dict = {}
        for i in range(len(nums)):
            if target - nums[i] in nums_dict:
                return nums_dict[target - nums[i]], i
            nums_dict[nums[i]] = i

    def pascal_triangle(self, numRows):
        """
        generates the first numRows of Pascal's triangle.
        :param numRows:
        :return: List[List[int]]
        """
        ret = []
        for i in range(numRows):
            ret.append(Solution().pascal_triangle_row(i))
        return ret

    def pascal_triangle_row(self, rowIndex):
        """
        preparation function for Solution().pascal_triangle()
        :param rowIndex: int
        :return: List[int]
        """
        ret = []
        for i in range(rowIndex + 1):
            ret.append(math.factorial(rowIndex) / (math.factorial(i) * math.factorial(rowIndex - i)))
        return ret

    def pascal_triangle2(self, num_rows):
        """
        another solution to pascal_triangle
        """
        ret = []
        for i in range(num_rows):
            ret.append([1])
            for j in range(1, i + 1):
                if j == i:
                    ret[i].append(1)
                else:
                    ret[i].append(ret[i - 1][j] + ret[i - 1][j - 1])
        return ret

    def majority_element(self, nums):
        """
        return the majority element (more than N/2 occurrences) of a list.
        :param nums: List[int]
        :return: int
        """
        items = list(set(nums))
        count = [nums.count(item) for item in items]
        count_max = max(count)
        if count_max > len(nums) / 2:
            return items[count.index(count_max)]
        else:
            return "No majority element"

    def majority_element2(self, nums):
        """
        return the majority element of a list, assuming that it exists.
        :param nums: List[int]
        :return: int
        """
        index = 0
        count = 1
        for i in range(1, len(nums)):
            if nums[index] == nums[i]:
                count += 1
            else:
                count -= 1
            if count == 0:
                index = i
                count += 1
        return nums[index]

    def max_sub_array(self, nums):
        """
        find the contiguous sub_array within an array which has the largest sum.
        :param nums: List[int]
        :return: int
        """
        candidate = nums[0]
        sum = nums[0]
        for i in range(1, len(nums)):
            if sum < 0:
                sum = nums[i]
            else:
                sum += nums[i]
            candidate = max(candidate, sum)
        return candidate

    def max_sub_array2(self, nums):
        """
        Solution 2 for max_sub_array, using recursion method.
        :param nums: List[int]
        :return: int
        """
        candidate = nums[0]
        sum = nums[0]
        for i in range(1, len(nums)):
            if sum < 0:
                candidate = max(Solution().max_sub_array2(nums[i:]), candidate)
            else:
                sum += nums[i]
                candidate = max(candidate, sum)
        return candidate

