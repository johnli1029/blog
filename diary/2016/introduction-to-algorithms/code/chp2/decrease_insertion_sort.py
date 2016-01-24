#coding:utf-8

def insertion_sort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i-1
        while j >= 0 and array[j] < key:    # 将原来的 array[j] > key 改为 array[j] < key
            array[j+1] = array[j]
            j -= 1
        array[j+1] = key


if __name__ == "__main__":

    import random

    array = list(range(7))
    random.shuffle(array)

    print("input = {0}".format(array))

    insertion_sort(array)
    
    print("output = {0}".format(array))
