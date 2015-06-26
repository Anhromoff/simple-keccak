from StateArray import *
from math import log

def Rnd(A, ir):
    return iota(chi(pi(ro(theta(A)))),ir)

class kec:
    b = 0
    nr = 0
    def __init__(self, b, nr):
        self.b = b
        self.nr = nr
    def __call__(self, s):
        assert len(s) == self.b
        a = StateArray(s)
        l = int(log(a.w,2))
        i = 0
        for ir in range(2*l+12-self.nr, 2*l+12):
            a = Rnd(a, ir)
        return a.bits

def Keccak_p(b, nr):
    return kec(b, nr)

def Keccak_f(b):
    assert b in [25, 50, 100, 200, 400, 8000, 1600]
    w = b/25
    l = int(log(w,2)) 
    return Keccak_p(b, 12+2*l)

def Sponge(f, pad, r):
    def s(M, d):
        p = BitArray(M)
        byte = []
        trail = BitArray()
        if len(p) % 8 != 0:
            parts = int(len(p)/8)
            trail = p[parts*8:]
        for i in range(int(len(p)/8)):
            b = p[i*8:(i+1)*8]
            b.reverse()
            byte.append(b)
        trail.reverse()
        byte.append(trail)
        p = BitArray().join(byte)
        
        p.append(pad(r, len(p)))
        c = f.b-r
        assert(len(p)%r == 0)

        parts = []
        for i in range(len(p)/r):
            parts.append(p[i*r: (i+1)*r])

        s = BitArray(f.b)
        for part in parts:
            s = s ^ (part + BitArray(c))
            s = f(s)
        Z = s[:r]
        while d > len(Z):
            Z += f(S)
        Z = Z[:d]
        
        byte = []
        for i in range(int(len(Z)/8)):
            b = Z[i*8:(i+1)*8]
            b.reverse()
            byte.append(b)
        Z = BitArray().join(byte)
        return Z

    return s

def pad101(x, m):
    j = (-m-2)%x
    return BitArray('0b1') + BitArray(j) + BitArray('0b1')

def Keccak(c):
    return Sponge(Keccak_p(1600,24), pad101, 1600-c)


