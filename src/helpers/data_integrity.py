def dictIsCorrupted(data_dict_labels, data_dict):
    # This functions checks whether the keys that will be used exist in the dictionary.
    for data_label in data_dict_labels:
        if data_label not in data_dict:
            return True
    return False