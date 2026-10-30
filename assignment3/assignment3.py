import random
import time
from enum import Enum


Algorithm = Enum("Algorithm", {"MERGESORT": "mergesort", "QUICKSORT": "quicksort"})


def merge_lists_together_in_desc_order(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort_recursive(chars):
    if len(chars) <= 1:
        return list(chars)
    mid = len(chars) // 2
    return merge_lists_together_in_desc_order(
        merge_sort_recursive(chars[:mid]), merge_sort_recursive(chars[mid:])
    )


def quicksort_recursive(chars, low, high):
    if low >= high:
        return
    lt, gt = split_list_into_two_smaller_left_and_right_and_pivot(chars, low, high)
    quicksort_recursive(chars, low, lt - 1)
    quicksort_recursive(chars, gt + 1, high)


def split_list_into_two_smaller_left_and_right_and_pivot(chars, low, high):
    # Middle pivot, then a 3-way split so repeated letters stay in one pass.
    mid = (low + high) // 2
    chars[low], chars[mid] = chars[mid], chars[low]
    pivot = chars[low]
    lt = low
    i = low + 1
    gt = high
    while i <= gt:
        if chars[i] < pivot:
            chars[lt], chars[i] = chars[i], chars[lt]
            lt += 1
            i += 1
        elif chars[i] > pivot:
            chars[gt], chars[i] = chars[i], chars[gt]
            gt -= 1
        else:
            i += 1
    return lt, gt


def sortString(string, algorithm=Algorithm.MERGESORT):
    chars = list(string)
    if algorithm is Algorithm.MERGESORT:
        # guarenteed O nlogn time, O n space
        return "".join(merge_sort_recursive(chars))
    if algorithm is Algorithm.QUICKSORT:
        # worst O n^2 time, O n space
        # average O nlogn time, O logn space
        quicksort_recursive(chars, 0, len(chars) - 1)
        return "".join(chars)


def groupAnagram(strings, algorithm=Algorithm.MERGESORT):
    """main function for grouping anagrams
    params:
        strings: List<String>: list of words we will work on
        algorithm: Algorithm: which sort to use
    return:
        List<List<String>>: list of lists of strings that are anagrams of each other
    """
    buckets = {}
    for word in strings:
        buckets.setdefault(sortString(word, algorithm), []).append(word)
    return list(buckets.values())


def format_results(groups):
    """
    format the results to be sorted and grouped
    since we allow the inner lists to be random order
    """
    return sorted(tuple(sorted(group)) for group in groups)


# simple testing on algorithms
def test_sort_string():
    words = [
        "",
        "a",
        "mango",
        "ogman",
        "bucket",
        "rat",
        "tar",
        "tango",
        "ogtan",
        "aaa",
        "Python",
        "a b",
        "zlkxcjpiqwnejlkasduo",
    ]
    for word in words:
        expected = "".join(sorted(word))
        assert sortString(word, Algorithm.MERGESORT) == expected
        assert sortString(word, Algorithm.QUICKSORT) == expected

    assert sortString("mango") == sortString("ogman") == "agmno"

    # build random strings for testing
    random_number_generator = random.Random(19283)
    for length in (0, 55, 67, 89, 200, 125, 256):
        for _ in range(20):
            word = "".join(
                chr(random_number_generator.randint(32, 126)) for _ in range(length)
            )
            expected = "".join(sorted(word))
            assert sortString(word, Algorithm.MERGESORT) == expected
            assert sortString(word, Algorithm.QUICKSORT) == expected


# testing groupAnagram
def test_group_anagram():
    sample = ["bucket", "rat", "mango", "tango", "ogtan", "tar"]
    expected = [["bucket"], ["rat", "tar"], ["mango"], ["tango", "ogtan"]]
    assert format_results(groupAnagram(sample)) == format_results(expected)
    assert format_results(groupAnagram(sample, Algorithm.QUICKSORT)) == format_results(
        expected
    )

    assert groupAnagram([]) == []
    assert groupAnagram([""]) == [[""]]
    assert groupAnagram(["solo"]) == [["solo"]]

    testing_words_1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    expected = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    assert format_results(groupAnagram(testing_words_1)) == format_results(expected)

    assert format_results(
        groupAnagram(["abc", "def", "cba", "fed", "xyz"])
    ) == format_results([["abc", "cba"], ["def", "fed"], ["xyz"]])
    assert format_results(groupAnagram(["", "b", ""])) == format_results(
        [["", ""], ["b"]]
    )
    # Comparison is by character code, so case stays distinct.
    assert format_results(groupAnagram(["ab", "AB", "ba"])) == format_results(
        [["ab", "ba"], ["AB"]]
    )

    testing_words_2 = [
        "mango",
        "ogman",
        "rat",
        "tar",
        "art",
        "bucket",
        "tango",
        "ogtan",
    ]
    assert format_results(
        groupAnagram(testing_words_2, Algorithm.MERGESORT)
    ) == format_results(groupAnagram(testing_words_2, Algorithm.QUICKSORT))


def set_timers_on_sorts_algs(samples, trials):
    time_each_algorithms = {}
    for algorithm in Algorithm:
        start = time.perf_counter()  # start timer for each algorithm
        for _ in range(trials):
            for sample in samples:
                sortString(sample, algorithm)
        # mark the time used
        time_each_algorithms[algorithm] = time.perf_counter() - start
    return time_each_algorithms


def compare_performance():
    rng = random.Random(241)

    def random_words(count, length):
        return [
            "".join(chr(rng.randint(97, 122)) for _ in range(length))
            for _ in range(count)
        ]

    short_words = random_words(400, 12)
    long_words = random_words(80, 400)
    sorted_words = [sortString(word) for word in long_words]

    scenarios = [
        ("random words", short_words, 5),
        ("longer random strings", long_words, 3),
        ("already sorted strings", sorted_words, 3),
    ]

    print("Performance comparison (mergesort vs quicksort)")
    for name, samples, trials in scenarios:
        timings = set_timers_on_sorts_algs(samples, trials)
        faster = min(timings, key=timings.get)
        slower = (
            Algorithm.QUICKSORT
            if faster is Algorithm.MERGESORT
            else Algorithm.MERGESORT
        )
        ratio = timings[slower] / timings[faster] if timings[faster] else 1.0
        length = len(samples[0]) if samples else 0
        print(f"  {name}: {len(samples)} strings, length {length}, {trials} trials")
        for algorithm in Algorithm:
            print(f"    {algorithm.value:10} {timings[algorithm]:.4f}s")
        print(f"    {faster.value} was {ratio:.2f}x faster")


def main():
    test_sort_string()
    test_group_anagram()
    print("All sample tests passed.")
    print()
    compare_performance()


if __name__ == "__main__":
    main()
