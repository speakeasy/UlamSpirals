from primes import primes
from matplotlib import pyplot as plt
import numpy as np
import scipy.misc

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
        f = False
        m = [[0x00] * n for i in range(n)]
        dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
        x, y = 0, -1
        c = n * n + self.start
        c = c * 2# + int((c * 0.5))
        c -= 2
        if c % 2 == 0:
            c -= 1
        for i in range(n + n - 1):
            for j in range((n + n - i) // 2):
                x += dx[i % 4]
                y += dy[i % 4]
                m[x][y] = 0xff
                print(c)
                if self.primes.is_prime(c):
                    m[x][y] = 0x00
                #if c == self.start:
                #    m[x][y] = 'X'
                c -= 2
                #if str(c).endswith("5"):
                #    c -= 2


        for i in range(self.size - 1, 0, -1):
            m[i] = m[i][::-1]

        m = m[::-1]
        return m

u = ulamspirals(1,20)

m = u.spiral_matrix(u.size)

plt.imshow(m, interpolation="nearest")
plt.gray()
plt.show()
#scipy.misc.toimage(m, str(u.size) + "x" + str(u.size) + "-s" + str(u.start) + ".png")

