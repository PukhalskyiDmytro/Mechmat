from math import factorial, log

def task_a(x, k):
    return x ** (2 * k) / factorial(2 * k)

def task_b(n):
    product = 1.0
    for i in range(1, n + 1):
        product *= (1 + 1 / (i ** 2))
    return product

def task_c(n, a, b):
    if n == 1:
        return a + b
    elif n == 2:
        return (a + b) ** 2 - a * b
    else:
        return (a + b) * task_c(n - 1, a, b) - (a * b) * task_c(n - 2, a, b)

def task_d(n):
    a = [1, 1, 1]
    while len(a) < n:
        a.append(a[-1] + a[-3])
    s_n = sum(a[k - 1] / factorial(2 * k) for k in range(1, n + 1))
    return s_n

def task_e(x, eps):
    approx = x
    n = 1
    term = x

    while term > eps:
        term = term * x**2 * (2*n-1) / (2*n+1)
        n += 1
        approx += term

    exact = log((1+x)/(1-x))
    return exact, 2*approx

if __name__ == "__main__":
    print(task_a(5, 3))
    print(task_b(50))
    print(task_c(5, 10, 10))
    print(task_d(6))
    print(task_e(0.5, 0.000001))