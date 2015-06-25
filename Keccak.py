from StateArray import *
from math import log

def Rnd(a, ir):
    return iota(chi(pi(ro(theta(A)))),ir)

def Keccak_p(b, nr):
    def kec(s):
        assert len(s) == b
        a = StateArray(s)
        l = int(log(a.w))
        for ir in range(2*l+12-nr, 2*l+12):
            a = Rnd(a, ir)
        return s.bits
    return kec

def keccak_f(b):
    assert b in [25, 50, 100, 200, 400, 8000, 1600]
    w = b/25
    l = int(log(w))
    return keccak_p(b, 12+2*l)
