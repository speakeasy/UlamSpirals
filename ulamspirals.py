from primes import primes
from matplotlib import pyplot as plt
import matplotlib.image as mpi
import numpy as np
from copy import copy, deepcopy
import pandas as pd
import scipy.misc

class ulamspirals:
    primes = None
    spiral = []
    size = None
    start = None
    mersp = [2,3,5,7,13,17,19,31]
    merx = []
    n = None
    mt = None
    usehtml = False

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
        if self.usehtml:
            self.n = np.array([[None] * n for i in range(n)])
            self.mt = [[None] * n for i in range(n)]
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

                #print(c)
                if self.usehtml:
                    self.n[x][y] = c

                if self.primes.is_prime(c):
                    if self.ismersennex(c):
                        m[x][y] = [0xff, 0x00, 0x00]
                        if self.usehtml:
                            self.mt[x][y] = 0x02
                    elif self.ismersennep(c):
                        m[x][y] = [0x00, 0xff, 0x00]
                        if self.usehtml:
                            self.mt[x][y] = 0x03
                    else:
                        m[x][y] = [0x00, 0x00, 0x00]
                        if self.usehtml:
                            self.mt[x][y] = 0x01
                else:
                    m[x][y] = [0xff, 0xff, 0xff]
                    if self.usehtml:
                        self.mt[x][y] = 0x00
                #if c == self.start:
                #    m[x][y] = 'X'
                c -= 2
                #if str(c).endswith("5"):
                #    c -= 2

        data = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        for i in range(self.size - 1, 0, -1):
            m[i] = m[i][::-1]
            if self.usehtml:
                self.n[i] = self.n[i][::-1]
                self.mt[i] = self.mt[i][::-1]
            for j in range(0, self.size - 1):
                data[i,j] = m[i][j]
        if self.usehtml:
            self.n = self.n[::-1]
            self.mt = self.mt[::-1]
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

def getclass(n):
    if n == 0:
        return "compound"
    if n == 1:
        return "prime"
    if n == 2:
        return "mprime"
    if n == 3:
        return "mprimex"

u = ulamspirals(1,3000)

m = u.spiral_matrix(u.size)

#print(m)
if u.usehtml:
    html = """<html>
    <head>
    <style>
    td { width: """ + str(100/u.size) + """%; padding-bottom: """ + str(100/u.size) + """%; height: 0; }
    td div { position: absolute }
    .compound { color: black; background-color: white; }
    .prime { color: white; background-color: black; }
    .mprime { color: black; background-color: red; }
    .mprimex { color: black; background-color: green; }
    </style>
    </head>
    <body>
    <table border="1" class="dataframe">
    <thead>
    <tr style="text-align: right;">
    <th></th>
    """

    for x in range(0, u.size - 1):
        html += "<th>" + str(x+1) + "</th>\n"
    html += "</tr>\n</thead>\n<tbody>\n"
    for x in range(0, u.size - 1):
        html += "<tr>\n<th>" + str(x+1) + "</th>\n"
        for y in range(0, u.size):
            html += "<td class=\"" + getclass(u.mt[x][y]) + "\">" + str(u.n[x][y]) + "</td>\n"
        html += "</tr>\n"

    html += "</tbody>\n</table>\n</body>\n</html>\n"
    print(html)
plt.imshow(m, interpolation="nearest")
#plt.gray()
plt.show()
mpi.imsave(str(u.size) + "x" + str(u.size) + "-s" + str(u.start) + ".png", m)


