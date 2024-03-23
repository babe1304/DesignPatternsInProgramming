from random import normalvariate
from math import ceil

class DistributionTester:
    def __call__(self, generator, percent):
        dist = generator()
        dist.sort()

        for p in range(10, 90, 10):
            print(f"{p}. percentil = {percent(dist, p)}")
        return

class Fibonacci:
    def __init__(self, n):
        self.n = n

    def __call__(self):
        return list(self.fib())

    def fib(self):
        a, b = 0, 1
        for _ in range(self.n):
            yield b
            a,b= b,a+b
        
class Random:
    def __init__(self, mu, sigma, n):
        self.mu = mu
        self.sigma = sigma
        self.n = n
        
    def __call__(self):
        return [round(normalvariate(self.mu, self.sigma)) for _ in range(self.n)]
    
class Linear:
    def __init__(self, lower_bound, upper_bound, dx):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.dx = dx

    def __call__(self):
        return list(range(self.lower_bound, self.upper_bound, self.dx))
    
class NearRank:
    def __call__(self, dist, p):
        n_p = ceil(p * len(dist) / 100) - 1
        return dist[n_p]
    
class LinInter:
    def __call__(self, dist, p):
        N = len(dist)
        p_i = [100 * (i - 0.5) / N for i in range(1, N + 1)]

        for i, pr in enumerate(p_i):
            if pr == p:
                return dist[i]
            if pr > p and p_i[i - 1] < pr:
                return dist[i - 1] + N * (p - p_i[i - 1])*(dist[i] - dist[i - 1])/100

if __name__=="__main__":
    distr = DistributionTester()

    fib = Fibonacci(50)
    rand = Random(10, 5, 50)
    lin = Linear(0, 100, 50)

    nr = NearRank()
    li = LinInter()

    print(fib()[:10])
    print("Fibonacci with NearRank")
    distr(fib, nr)
    print("Fibonacci with LinearInterpoaltion")
    distr(fib, li)
    print("Random with LinearInterpoaltion")
    distr(rand, li)
    print("Linear with NearRank")
    distr(lin, nr)
    print("Linear with LinearInterpoaltion")
    distr(lin, li)