def find_first_and_last(nums, target):
    def leftmost():
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            left, right = (mid + 1, right) if nums[mid] < target else (left, mid)
        return left

    def rightmost():
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            left, right = (mid + 1, right) if nums[mid] <= target else (left, mid)
        return left

    start = leftmost()
    return (
        [-1, -1]
        if start == len(nums) or nums[start] != target
        else [start, rightmost() - 1]
    )


def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    rows = len(matrix)
    cols = len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        mid = (left + right) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        left, right = (mid + 1, right) if value < target else (left, mid - 1)
    return False


def test_task1():
    # Examples from the assignment.
    assert find_first_and_last([4, 9, 10, 13, 17, 17, 19, 21], 17) == [4, 5]
    assert find_first_and_last([2, 4, 6, 8, 10, 14, 16], 12) == [-1, -1]
    assert find_first_and_last([], 0) == [-1, -1]

    # Target occupies one cell, the whole array, or an end of the array.
    assert find_first_and_last([5], 5) == [0, 0]
    assert find_first_and_last([5], 3) == [-1, -1]
    assert find_first_and_last([1, 1, 1, 1], 1) == [0, 3]
    assert find_first_and_last([1, 2, 2, 2, 3], 2) == [1, 3]
    assert find_first_and_last([2, 2, 2, 3, 4], 2) == [0, 2]
    assert find_first_and_last([1, 3, 5, 7, 7], 7) == [3, 4]

    # Target is outside the range of values in the array.
    assert find_first_and_last([2, 4, 6], 1) == [-1, -1]
    assert find_first_and_last([2, 4, 6], 8) == [-1, -1]
    assert find_first_and_last([-3, -1, 0, 2], -1) == [1, 1]


def test_task2():
    matrix = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60],
    ]

    assert search_matrix(matrix, 3) is True
    assert search_matrix(matrix, 13) is False
    assert search_matrix(matrix, 1) is True
    assert search_matrix(matrix, 60) is True
    assert search_matrix(matrix, 11) is True
    assert search_matrix(matrix, 0) is False
    assert search_matrix(matrix, 61) is False
    assert search_matrix(matrix, 21) is False

    # One cell, one row, one column, and empty inputs.
    assert search_matrix([[7]], 7) is True
    assert search_matrix([[7]], 8) is False
    assert search_matrix([[1, 3, 5]], 5) is True
    assert search_matrix([[1, 3, 5]], 2) is False
    assert search_matrix([[1], [3], [5]], 3) is True
    assert search_matrix([[1], [3], [5]], 4) is False
    assert search_matrix([], 1) is False
    assert search_matrix([[]], 1) is False


def main():
    test_task1()
    test_task2()
    print("All sample tests passed.")


if __name__ == "__main__":
    main()
