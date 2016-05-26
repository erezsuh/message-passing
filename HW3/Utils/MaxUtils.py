
def argmax(vector):
    current_max = 0
    current_index = 0
    for i, val in enumerate(vector):
        if val > current_max:
            current_index = i
            current_max = val
    return current_index, current_max
