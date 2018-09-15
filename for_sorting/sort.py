#!/usr/bin/env python


class Sort:

    def __init__(self, my_list):
        self.my_list = my_list

    def bubble_sort(self):
        if len(self.my_list) > 1:
            for i in range(len(self.my_list)-1):
                for j in range(len(self.my_list)-1-i):
                    if self.my_list[j] > self.my_list[j+1]:
                        self.my_list[j], self.my_list[j+1] = self.my_list[j+1], self.my_list[j]
        return self.my_list

    def select_sort(self):
        if len(self.my_list) > 1:
            for index in range(len(self.my_list)):
                for i in range(index, len(self.my_list)):
                    if self.my_list[index] > self.my_list[i]:
                        self.my_list[index], self.my_list[i] = self.my_list[i], self.my_list[index]
        return self.my_list

    def insert_sort1(self):
        if len(self.my_list) > 1:
            for index in range(len(self.my_list)):
                for i in range(index, 0, -1):
                    if self.my_list[i] < self.my_list[i-1]:
                        self.my_list[i-1], self.my_list[i] = self.my_list[i], self.my_list[i-1]
        return self.my_list

    def shell_sort(self):
        if len(self.my_list) > 1:
            distance = len(self.my_list)//2
            while distance > 0:
                for index in range(0, len(self.my_list), distance):
                    for i in range(index, 0, -distance):
                        if self.my_list[i] < self.my_list[i - distance]:
                            self.my_list[i - distance], self.my_list[i] = self.my_list[i], self.my_list[i - distance]
                distance //= 2
        return self.my_list

    def heap_sort(self):
        """get the index of left and right data"""
        for i in range(0, len(self.my_list)):
            index = (len(self.my_list) - i - 2) // 2
            for root in range(index, -1, -1):
                if (2*root+2) < (len(self.my_list)-i) and self.my_list[2*root+2] > self.my_list[2*root+1]:
                    mark = 2 * root + 2
                else:
                    mark = 2 * root + 1
                if self.my_list[root] > self.my_list[mark]:
                    mark = root
                if mark != root:
                    self.my_list[root], self.my_list[mark] = self.my_list[mark], self.my_list[root]
                else:
                    continue
            self.my_list[0], self.my_list[len(self.my_list)-1-i] = self.my_list[len(self.my_list)-1-i],  self.my_list[0]
        return self.my_list

    def quick_sort(self):

        def quicksort(left, right, mylist):

            print(left, right)
            if left >= right:
                return
            else:
                benchmark = mylist[left]
                low = left
                high = right
                while left < right:
                    while left < right and mylist[right] >= benchmark:
                        right -= 1
                    mylist[left] = mylist[right]
                    while left < right and mylist[left] <= benchmark:
                        left += 1
                    mylist[right] = mylist[left]
                mylist[right] = benchmark
                quicksort(low, left-1, mylist)
                quicksort(left+1, high, mylist)

        quicksort(0, len(self.my_list) - 1, self.my_list)
        return self.my_list





















