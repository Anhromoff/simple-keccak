from StateArray import *
from math import log

def Rnd(a, ir):
    return iota(chi(pi(ro(theta(A)))),ir)

class kec:
    b = 0
    def __init__(self, b):
        self.b = b
    def __call__(self, s):
        assert len(s) == b
        a = StateArray(s)
        l = int(log(a.w))
        for ir in range(2*l+12-nr, 2*l+12):
            a = Rnd(a, ir)
        return a.bits

def Keccak_p(b, nr):
    return kec(b)

def keccak_f(b):
    assert b in [25, 50, 100, 200, 400, 8000, 1600]
    w = b/25
    l = int(log(w))
    return keccak_p(b, 12+2*l)

def Sponge(f, pad, r):
    def s(M, d):
        p = BitArray(M)
        p.append(pad(r, p))
        c = f.b-r
        assert(len(p)%r == 0)

        parts = []
        for i in range(p/r):
            parts.append(p[i*r: (i+1)*r])

        s = BitArray(f.b)
        for part in parts:
            s = f(s ^ (part + BitArray(c)))
        Z = s[:r]
        while d > len(Z):
            Z += f(S)
        return Z[:d]

    return s

def pad101(x, m):
    j = (-m-2)%x
    return BitArray('0b1') + BitArray(j) + BitArray('0b1')
