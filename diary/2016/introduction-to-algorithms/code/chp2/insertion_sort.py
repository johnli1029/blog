#coding:utf-8

def insertion_sort(array):
    for i in range(1, len(array)):          # 产生一个 1..array.length 的序列
        key = array[i]                      # 获取被排序的键
        j = i-1                             # 将被排序的键与排在它前面的数组元素进行比较
        while j >= 0 and array[j] > key:    # 如果排在前面的元素有比被排序键更大的元素
            array[j+1] = array[j]           # 那么将这些元素移动到数组靠后的位置
            j -= 1                          # 一直执行以上操作，直到发现比被排序键更小的元素为止
        array[j+1] = key                    # 最后将被排序键放到它应该在的位置上


if __name__ == "__main__":

    import random

    array = list(range(7))
    random.shuffle(array)

    print("input = {0}".format(array))

    insertion_sort(array)
    
    print("output = {0}".format(array))
