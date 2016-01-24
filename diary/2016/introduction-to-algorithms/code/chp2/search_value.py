#coding:utf-8

def search_value(array, value):
    i = None
    for j in range(len(array)):
        if array[j] == value:
            i = j
            break
    return i


if __name__ == "__main__":

    import random

    array = list(range(6))
    random.shuffle(array)

    value1 = random.choice(array)
    value2 = 10086

    print("find {0} in {1}, i = {2}.".format(value1, array, search_value(array, value1)))

    print("find {0} in {1}, i = {2}.".format(value2, array, search_value(array, value2)))
