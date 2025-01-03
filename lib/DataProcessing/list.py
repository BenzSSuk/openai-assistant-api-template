
def filter_list(list_in, filter_str):
    list_out = []

    for element in list_in:
        if filter_str in element:
            list_out.append(element)

    return list_out