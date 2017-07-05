MEMORY_MB_MAX = 4096
import gmpy2


class primes:
    def __init__(self):
        self._known_primes = [2, 3, 325, 9375, 28178, 450775, 9780504, 1795265022]
        self._known_primes += [x for x in range(5, 1000, 2) if self.is_prime(x)]

    def factor(self, n, p=2):
        s = 0
        d = n - 1
        q = p
        while not d & q - 1:
            s += 1
            q *= p
        return s, d // (q // p)

    def _try_composite(self, a, d, n, s):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True  # n  is definitely composite

    def is_prime(self, n, _precision_for_huge_n=16):
        if n < 0:
            return False
        if n in self._known_primes or n in (0, 1):
            return True
        if any((n % p) == 0 for p in self._known_primes):
            return False
        d, s = n - 1, 0
        while not d % 2:
            d, s = d >> 1, s + 1
        # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
        if d < 0:
            d = d * -1.0
        if n < 1373653:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3))
        if n < 25326001:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5))
        if n < 118670087467:
            if n == 3215031751:
                return False
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7))
        if n < 2152302898747:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
        if n < 3474749660383:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
        if n < 341550071728321:
            return not any(self._try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
        # otherwise
        return not any(self._try_composite(a, d, n, s)
                       for a in self._known_primes[:_precision_for_huge_n])

    def sieve(self, end):
        prime_list = [2, 3]
        sieve_list = [True] * (end + 1)
        for each_number in self.candidate_range(self, end):
            if sieve_list[each_number]:
                prime_list.append(each_number)
                for multiple in range(each_number * each_number, end + 1, each_number):
                    sieve_list[multiple] = False
        return prime_list

    def candidate_range(self, n):
        cur = 5
        incr = 2
        while cur < n + 1:
            yield cur
            cur += incr
            incr ^= 6  # or incr = 6-incr, or however

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