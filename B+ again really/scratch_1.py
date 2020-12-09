from game_classes import Wheel
from itertools import cycle
import errno
import os

DIR = r"C:\Users\User1\Desktop\FP Project3.7"
# DIR = os.getcwd()
#
# instance = Wheel()
#
# print(instance.abc)

list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]

dict1 = cycle({
    key: val for key, val in zip(list1, list2)
})

dict2 = {
    key: val for key, val in zip(list1, list2)
}

print(dict1)
print(dict2)
