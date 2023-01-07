from reorder import reorder_pages

input_1 = 1
expected_output_1 = [-1, 0, -1, -1]

input_4 = 4
expected_output_4 = [3, 0, 1, 2]

input_9 = 9
expected_output_9 = [-1, 0, 1, -1, -1, 2, 3, 8, 7, 4, 5, 6]

input_21 = 21
expected_output_21 = [-1, 0, 1, -1, -1, 2, 3, 20, 19, 4, 5, 18, 17, 6, 7, 16, 15, 8, 9, 14, 13, 10, 11, 12]

assert reorder_pages(input_1) == expected_output_1
assert reorder_pages(input_4) == expected_output_4
assert reorder_pages(input_9) == expected_output_9
assert reorder_pages(input_21) == expected_output_21

print('All tests successful')
