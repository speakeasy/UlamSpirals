from primes import primes
import numpy as np

class ulamspirals:
    primes = None
    spiral = []
    size = None
    start = None

    def __init__(self, start, size=1024):
        if size % 2 == 0:
            size += 1
        self.primes = primes()
        self.size = size
        if start < 0:
            start = 0
        self.start = start

    def spiral_matrix(self, n):
        m = [[0x00] * n for i in range(n)]
        dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
        x, y = 0, -1
        c = n * n + self.start - 1
        for i in range(n + n - 1):
            for j in range((n + n - i) // 2):
                x += dx[i % 4]
                y += dy[i % 4]
                m[x][y] = 0x00
                if self.primes.is_prime(c):
                    m[x][y] = 0x01
                if c == self.start:
                    m[x][y] = 'X'
                c -= 1

        for i in m:
            i.reverse
        m.reverse
        return m

u = ulamspirals(1, 20)

m = u.spiral_matrix(u.size)

for row in m:
    print(*row)