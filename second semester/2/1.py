import math

#1
def task_1 ():
    string = input()
    result = string[0]
    for i in range(1, len(string)):
        if string[i] != string[i-1]:
            result += string[i]
    print(result)

#2
def is_prime(n):
    for k in range(math.floor(math.sqrt(n))+1):
        if n % k == 0:
            return False
    return True

def invert_number(n):
    return int(str(n)[::-1])

def task_2():
    a, b = map(int, input().split())
    result = 0
    for i in range(min(a,b), max(a,b)+1):
        if is_prime(i) and is_prime(invert_number(i)):
            result += 1

    print(result)

#3
def task_3():
    string = input()
    max_char = max(string)
    number_of_rep = string.count(max_char)

    print(f"{max_char} {number_of_rep}")
