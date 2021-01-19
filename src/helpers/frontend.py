def fixColumnCount(array, cols_amount):
    fixed_array = list()
    i = 0
    fixer = 0
    tmp = list()
    while(i<len(array)):
        tmp.append(array[i])

        fixer += 1
        if fixer == cols_amount:
            fixer = 0
            fixed_array.append(tmp)
            tmp = list()

        i += 1
    if len(tmp) > 0:
        fixed_array.append(tmp)
    return fixed_array