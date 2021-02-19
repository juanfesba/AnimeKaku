def fixColumnCount(iterable, cols_amount):
    fixed_array = list()
    fixer = 0
    tmp = list()
    for element in iterable:
        tmp.append(element)

        fixer += 1
        if fixer == cols_amount:
            fixer = 0
            fixed_array.append(tmp)
            tmp = list()
    if fixer > 0:
        fixed_array.append(tmp)
    return fixed_array