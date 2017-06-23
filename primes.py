class primes:
    def factor(self, n, p=2):
        s = 0
        d = n - 1
        q = p
        while not d & q - 1:
            s += 1
            q *= p
        return s, d // (q // p)

    def primes_sieve(self, limit):
        limitn = limit + 1
        not_prime = set()
        primes = []
        for i in range(2, limitn):
            if i in not_prime:
                continue
            for f in range(i * 2, limitn, i):
                not_prime.add(f)
            primes.append(i)
        return primes

    def strong_pseudoprime(self, n, a, s=None, d=None):
        if (s is None) or (d is None):
            s, d = self.factor(n, 2)
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return x == n - 1

    def baillie_psw(self, n, limit=100):
        if not n & 1:
            return False
        if n < 2 or self.is_square(n):
            return False
        for i in range(3, limit + 1, 2):
            if n % i:
                return n == i
        return self.strong_pseudoprime(n, 2) and self.strong_lucas_pseudoprime(n)

    def jacobi(self, a, p):
        if (not p & 1) or (p < 0):
            raise ValueError('p must be a positive odd number.')
        if (a == 0) or (a == 1):
            return a
        a = a % p
        t = 1
        while a != 0:
            while not a & 1:
                a >>= 1
                if p & 7 in (3, 5):
                    t = -t
            a, p = p, a
            if (a & 3 == 3) and (p & 3) == 3:
                t = -t
            a = a % p
        if p == 1:
            return t
        return 0

    def strong_lucas_pseudoprime(self, n):
        d, p, q = self.selfridge(n)
        if p == 0:
            return n == d

        s, t = self.factor(n)

        u, v, k = self.chain(n, 1, p, 1, p, d, q, t >> 1)

        if (u == 0) or (v == 0):
            return True

        for i in range(1, s):
            v = (v * v - 2 * k) % n
            k = (k * k) % n
            if v == 0:
                return True

        return False

    def chain(self, n, u1, v1, u2, v2, d, q, m):
        k = q
        while m > 0:
            u2 = (u2 * v2) % n
            v2 = (v2 * v2 - 2 * q) % n
            q = (q * q) % n
            if m & 1 == 1:
                t1, t2 = u2 * v1, u1 * v2
                t3, t4 = v2 * v1, u2 * u1 * d
                u1, v1 = t1 + t2, t3 + t4
                if u1 & 1 == 1:
                    u1 = u1 + n
                if v1 & 1 == 1:
                    v1 = v1 + n
                u1, v1 = (u1 / 2) % n, (v1 / 2) % n
                k = (q * k) % n
            m = m >> 1
        return u1, v1, k

    def is_square(self, n):
        s = self.isqrt(n)
        return s * s == n

    def isqrt(self, n):
        if n < 0:
            raise ValueError('Square root is not defined for negative numbers.')
        x = int(n)
        if x == 0:
            return 0
        a, b = divmod(x.bit_length(), 2)
        n = 2 ** (a + b)
        while True:
            y = (n + x // n) >> 1
            if y >= n:
                return n
            n = y
