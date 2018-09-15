#!/usr/bin/env python


class Insert:

    def __init__(self, my_list, my_num):
        self.my_list = my_list
        self.my_num = my_num

    def insert_num(self, num):
        """insert a num to a """
        if len(self.my_list) == 0:
            self.my_list.append(num)
        else:
            for i in range(len(self.my_list)):
                if self.my_list[i] > num:
                    self.my_list[i+1:] = self.my_list[i:]
                    self.my_list[i] = num
                    break
                else:
                    if i == (len(self.my_list)-1):
                        self.my_list.append(num)
        return self.my_list

    def insert_list(self, my_list):
        for i in my_list:
            self.insert_num(i)
        return self.my_list





