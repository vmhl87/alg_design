# recursive solution
def fib_recursive(n):
    if n == 0: return 0
    if n == 1: return 1
    return fib_recursive(n-1) + fib_recursive(n-2)

# bottom-up dp accelerated
def fib_dp(n):
    dp = [0, 1]
    for i in range(2, n+1):
        dp.append(dp[-1] + dp[i-2])
    return dp[-1]

# bottom-up with memory saving
def fib_dp_memsave(n):
    if n == 0: return a
    a, b = 0, 1
    for i in range(2, n+1):
        a, b = b, a+b
    return b

# O(log n) by matrix multiplication
def fib_matrix(n):
    mat, vec = [[1, 1], [1, 2]], [0, 1]
    m = n // 2
    while m:
        if m%2 == 1:
            vec = vmul(vec, mat)
        mat = mmul(mat, mat)
        m //= 2
    return vec[n%2]

# matrix utilities - assumed 2x2

def vmul(v, m): # vector by matrix
    return [
        m[0][0]*v[0] + m[0][1]*v[1],
        m[1][0]*v[0] + m[1][1]*v[1]
    ]

def mmul(m1, m2): # matrix by matrix
    return [
        [
            m1[0][0]*m2[0][0] + m1[0][1]*m2[1][0],
            m1[0][0]*m2[0][1] + m1[0][1]*m2[1][1]
        ],
        [
            m1[1][0]*m2[0][0] + m1[1][1]*m2[1][0],
            m1[1][0]*m2[0][1] + m1[1][1]*m2[1][1]
        ]
    ]
