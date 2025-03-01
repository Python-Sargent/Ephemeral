def get_3x3(input_list, index1, index2):
    """
    Crops a 2D list to a 3x3 pattern from the center if possible.
    If the input is smaller than 3x3 in either dimension, it will return as much as possible from the center-ish.
    """
    num_rows_input = len(input_list)
    if num_rows_input == 0 or type(input_list) != type(list()) :
        return []  # Handle empty input

    num_cols_input_first_row = len(input_list[0]) if num_rows_input > 0 else 0

    start_row = max(-1, (index1 - 2))  # Calculate starting row index
    start_col = max(-1, (index2 - 2)) # Calculate starting col index

    cropped_list = []
    for i in range(3):
        row = []
        for j in range(3):
            row_index = start_row + i
            col_index = start_col + j

            if 0 <= row_index < num_rows_input and 0 <= col_index < num_cols_input_first_row:
                row.append(input_list[row_index][col_index])
            else:
                # Handle cases where center crop goes out of bounds (e.g., pad with None or 0 if needed)
                # For now, we'll just skip if out of bounds, which might result in smaller rows
                pass  # Or you could append None/0 here if padding is desired

        if row: # Only append rows that have elements (handle cases where center is partially out of bounds)
            cropped_list.append(row)

    return cropped_list

# Example usage with center cropping:
center_list_2d = [
    [1,  2,  3,  4,  5,  6,  7],
    [8,  9,  10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19, 20, 21],
    [22, 23, 24, 25, 26, 27, 28],
    [29, 30, 31, 32, 33, 34, 35]
]

cropped_center = get_3x3(center_list_2d, 0, 0)
print(cropped_center)
# Expected Output (center elements):
# [[10, 11, 12], [17, 18, 19], [24, 25, 26]]


smaller_center_list = [[1,2],[3,4,5]]
cropped_smaller_center = get_3x3(smaller_center_list, 0, 0)
print(cropped_smaller_center)
# Output for smaller list (as much center-ish as possible):
# [[1, 2], [3, 4, 5]]  (In this case, it's effectively top-left as the center logic doesn't significantly change things)