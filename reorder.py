from math import ceil

def reorder_pages(num_pages):
    num_sheets = ceil(num_pages / 4)
    printed_pages = num_sheets * 4
    new_order = []

    for sheet in range(num_sheets):
        last_not_printed_page = printed_pages - (2 * sheet) - 1
        next_not_printed_page = sheet * 2
        second_not_printed_page = sheet * 2 + 1
        second_last_not_printed_page = printed_pages - (2 * sheet) - 2

        new_order.append(last_not_printed_page)
        new_order.append(next_not_printed_page)
        new_order.append(second_not_printed_page)
        new_order.append(second_last_not_printed_page)

    new_order = [x if x <= num_pages -1 else -1 for x in new_order]
    return new_order
