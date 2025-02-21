def find_by_id(data_list, item_id):
    for item in data_list:
        if item.id == item_id:
            return item
    return None
