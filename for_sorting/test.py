#!/usr/bin/env python
import random
import numpy as np
from sort import Sort
from insert import Insert

if __name__ == '__main__':
    list_test = np.random.randint(10, size=5).tolist()
    num_test = random.randint(1, 7)

    print("this is the list you want to sort: " + str(list_test))
    # print("this is the number you want to insert: " + str(num_test))

    "get the list sorted"
    my_sort = Sort(list_test)
    print(my_sort.quick_sort())

    "insert the number and then insert the list"
    """
    my_insert = Insert(list_test, num_test)
    print(my_insert.insert_num(num_test))
    print(my_insert.insert_list([7, 8, 9]))
    """