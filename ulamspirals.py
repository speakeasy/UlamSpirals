from primes import primes
from matplotlib import pyplot as plt
import numpy as np
import scipy.misc

class ulamspirals:
    primes = None
    spiral = []
    size = None
    start = None
    mersp = [2,3,5,7,13,17,19,31]
    merx = []

    def __init__(self, start, size=1024):
        if size % 2 == 0:
            size += 1
        self.primes = primes()
        self.size = size
        if start < 0:
            start = 0
        self.start = start
        for i in self.mersp:
            self.merx.append(2**i-1)

    def spiral_matrix(self, n):
        f = False
        m = np.array([[None] * n for i in range(n)])
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

                print(c)
                if self.primes.is_prime(c):
                    if self.ismersennex(c):
                        m[x][y] = [0xff, 0x00, 0x00]
                    elif self.ismersennep(c):
                        m[x][y] = [0x00, 0xff, 0x00]
                    else:
                        m[x][y] = [0x00, 0x00, 0x00]
                else:
                    m[x][y] = [0xff, 0xff, 0xff]
                #if c == self.start:
                #    m[x][y] = 'X'
                c -= 2
                #if str(c).endswith("5"):
                #    c -= 2

        data = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        for i in range(self.size - 1, 0, -1):
            m[i] = m[i][::-1]
            for j in range(0, self.size - 1):
                data[i,j] = m[i][j]
        m = m[::-1]
        for i in range(0,self.size):
            for j in range(0, self.size):
                data[i,j] = m[i][j]
        return data

    def ismersennep(self, n):
        for i in self.mersp:
            if n == i:
                return True
        return False

    def ismersennex(self, n):
        for i in self.merx:
            if n == i:
                return True
        return False


u = ulamspirals(1,3000)

m = u.spiral_matrix(u.size)

print(m)
plt.imshow(m, interpolation="nearest")
#plt.gray()
plt.show()
#scipy.misc.toimage(m, str(u.size) + "x" + str(u.size) + "-s" + str(u.start) + ".png")

