def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def is_power_of_five(n):
    if n <= 0:
        return False
    while n % 5 == 0:
        n //= 5
    return n == 1