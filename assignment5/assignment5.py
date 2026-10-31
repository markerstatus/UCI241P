def contains_permutation(s1, s2):
    """Return True if some permutation of s1 is a substring of s2.

    params:
        s1: string whose rearrangement we look for
        s2: string to search
    return:
        bool

    explain: A walking window e.g.
    ------------------------
    ⬇
    e  i  b  a  c  x  l  p
    ------------------------

    char counting data structure: list of 26 zeros. [0,0,0,...]
    corresponding to each english letter a-z

    for each ord of a char from s1, +1 of the corresponding index
    and we walk through s2 one by one, until we find a index which need === window
    """
    if len(s1) > len(s2):
        return False
    if not s1:
        return True

    need = [0] * 26
    walker_window = [0] * 26

    for char in s1:
        need[ord(char) - ord("a")] += 1

    width = len(s1)
    for index, char in enumerate(s2):
        walker_window[ord(char) - ord("a")] += 1
        if index >= width:
            # delete the previous added char which is now falls outside window
            walker_window[ord(s2[index - width]) - ord("a")] -= 1
        if index >= width - 1 and walker_window == need:
            # we found a permutation of s1 in s2
            return True
    return False


def valid_queen_boards():
    """Return every safe 8-queens placement as row numbers, one per column.

    Rows are 1-based and columns stay in order 1 through 8. A placement is safe
    when each row is used once and no two queens share a diagonal.
    """
    boards = []
    rows = [0] * 8
    used_row = [False] * 8

    def place(column):
        # column runs from 0 to 7 while a row is still being chosen.
        # place(0) fills the first column. column == 8 means all eight queens are placed.
        if column == 8:
            # rows holds 0..7. Board numbers in the assignment are 1..8, so add 1.
            # [0, 4, 7, 5, 2, 6, 1, 3] is saved as [1, 5, 8, 6, 3, 7, 2, 4].
            boards.append([row + 1 for row in rows])
            return
        # Try every row in this column. Take the first safe one and go deeper.
        # If a later column gets stuck, execution returns here and the loop tries the next row.
        for row in range(8):
            # A used row means an earlier column already has a queen there.
            # Column 0 taking row 0 makes column 1 skip row 0.
            if used_row[row]:
                continue
            # A diagonal attack is a row gap equal to the column gap.
            # The queen at column 0, row 0 blocks column 1, row 1,
            # because abs(0 - 1) == 1 - 0.
            if any(
                abs(rows[prev_queen_col] - row) == column - prev_queen_col
                for prev_queen_col in range(column)
            ):
                continue
            # This row is safe with every queen already on the board. Record it and fill the next column.
            used_row[row] = True
            rows[column] = row
            place(column + 1)
            # Backtrack. Clear this queen so the loop can try the next row in the same column.
            # The next successful try overwrites rows[column].
            used_row[row] = False

    place(0)
    return boards


QUEEN_BOARDS = valid_queen_boards()


def min_queen_moves(rows):
    """Return the fewest vertical moves that leave the eight queens non-attacking.

    Each queen may change row only. One move sends a queen from its current row
    to any other row in the same column.

    params:
        rows: eight integers in 1..8, the current row of the queen in each column
    return:
        int: minimum number of queens that must change row


    explain:
    board is a [1,2,3,4,5,6,7,8] which is a valid 8-queens placement board we stored earlier
    zip is combining our valid board with the rows passed in: [(1,2), (3,4), ...]
    for each tuple pair, we gonna reduce that into True and False based on if they are different
    then we sum that list [True, False, ...] to get a number like 4
    we do this validation for every board against rows.
    and we take the minimum of that list [1,4,6,2, ......]
    Then we will have the answer
    """
    return min(
        sum(
            possible_position_we_are_testing != valid_position
            for possible_position_we_are_testing, valid_position in zip(rows, board)
        )
        for board in QUEEN_BOARDS
    )


def test_contains_permutation():
    assert contains_permutation("ab", "eidbaooo") is True
    assert contains_permutation("ab", "eidboaoo") is False
    assert contains_permutation("ab", "bacdefgh") is True
    assert contains_permutation("ab", "cdefghba") is True
    assert contains_permutation("abc", "abc") is True
    assert contains_permutation("abcd", "abc") is False
    assert contains_permutation("c", "ab") is False
    assert contains_permutation("c", "abc") is True


def test_min_queen_moves():
    assert len(QUEEN_BOARDS) == 92
    assert min_queen_moves([1, 2, 3, 4, 5, 6, 7, 8]) == 7
    assert min_queen_moves([1, 1, 1, 1, 1, 1, 1, 1]) == 7
    assert min_queen_moves([1, 5, 8, 6, 3, 7, 2, 4]) == 0


def main():
    test_contains_permutation()
    test_min_queen_moves()
    print("All sample tests passed.")


if __name__ == "__main__":
    main()
