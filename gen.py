import os.path
import random
import string
import timeit

# with open("C:/Users/38098/PycharmProjects/numbers.txt", "w") as f_write:
#     letters = string.ascii_letters
#     while os.stat(file_name).st_size < 50000000:
#         item = random.choice([random.choice(string.ascii_letters), random.randint(0, 100)])
#         f_write.write(f'{item}  ')

test = """
value = 0
with open("C:/Users/38098/PycharmProjects/numbers.txt", "r") as f_read:
    for line in f_read.readlines():
        if line.strip().isdigit():
            value += int(line.strip())
"""
print(timeit.timeit(test, number=10))

test = """
value = 0
with open("C:/Users/38098/PycharmProjects/numbers.txt", "r") as f_read:
    for line in f_read:
        if line.strip().isdigit():
            value += int(line.strip())
"""
print(timeit.timeit(test, number=10))

test = """
value = 0
with open("C:/Users/38098/PycharmProjects/numbers.txt", "r") as f_read:
    numbers = (int(line.strip()) for line in f_read if line.strip().isdigit())
    value = sum(numbers)
"""
print(timeit.timeit(test, number=10))
