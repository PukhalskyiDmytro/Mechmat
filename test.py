from itertools import permutations

def tau(perm, k):
    for i in range(1, perm[k-1]):
        k = perm[k - 1]
    return k

def find_min_max_tau_sum(n):
    min_sum = float('inf')
    max_sum = float('-inf')
    min_perm = None
    max_perm = None

    for perm in permutations(range(1, n + 1)):
        tau_sum = sum(tau(perm, k) for k in range(1, n + 1))
        if tau_sum < min_sum:
            min_sum = tau_sum
            min_perm = perm
        if tau_sum > max_sum:
            max_sum = tau_sum
            max_perm = perm

    return min_sum, max_sum, min_perm, max_perm


n = 3
min_tau_sum, max_tau_sum, min_perm, max_perm = find_min_max_tau_sum(n)
print(f"Мінімальна сума: {min_tau_sum}, Перестановка: {min_perm}")
print(f"Максимальна сума: {max_tau_sum}, Перестановка: {max_perm}")
