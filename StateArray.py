from bitstring import BitArray
from math import log

class StateArray:
    bits = 0
    w = 0
    def __init__(self, bits):
        self.bits = BitArray(bits[:])
        assert len(self.bits) in [25, 50, 100, 200, 400, 800, 1600]
        self.w = len(self.bits)/25
    
    def bit(self, x, y, z):
        assert x < 5
        assert y < 5
        assert z < self.w
        return self.bits[self.w*(5*y+x) + z]
    
    def setBit(self, x, y, z, val):
        assert x < 5
        assert y < 5
        assert z < self.w
        self.bits[self.w*(5*y+x) + z] = val

    def lane(self, x, y):
        assert x < 5
        assert y < 5
        offset = self.w*(5*y+x)
        return self.bits[offset : offset+self.w]

    def row(self, y, z):
        r = BitArray()
        for x in range(5):
            r += self.bit(x,y,z)
        return r

    def copy(self):
        return StateArray(self.bits[:])

def theta(a):
    retA = a.copy()
    C = []
    #passo 1
    for x in range(5):
        C.append([]) 
        for z in range(a.w):
            C[x].append(a.bit(x, 0, z)
                      ^ a.bit(x, 1, z)        
                      ^ a.bit(x, 2, z)        
                      ^ a.bit(x, 3, z)        
                      ^ a.bit(x, 4, z))        
    D = []
    #passo 2
    for x in range(5):
        D.append([]) 
        for z in range(a.w):
            D[x].append(C[(x-1)%5][z] ^ C[(x+1)%5][(z-1)%a.w])
    
    #passo 3
    for x in range(5):
        for y in range(5):
            for z in range(a.w):
                retA.setBit(x, y, z, a.bit(x, y, z) ^ D[x][z])

    return retA 

def ro(a):
    retA = a.copy()
    x, y = (1, 0)
    for t in range(0, 24):
        #print x, y, ((t+1)*(t+2)/2) 
        for z in range(0, a.w):
            retA.setBit(x,y,z, a.bit(x, y, (z-(t+1)*(t+2)/2) % a.w))
        x, y = (y, (2*x + 3*y) % 5)
    return retA

def pi(a):
    retA = a.copy()
    for x in range(5):
        for y in range(5):
            for z in range(a.w):
                retA.setBit(x,y,z, a.bit((x+3*y)%5, x, z))
    return retA

def chi(a):
    retA = a.copy()
    for x in range(5):
        for y in range(5):
            for z in range(a.w):
                nx1 = not a.bit((x+1)%5, y, z)
                x2 = a.bit((x+2)%5, y, z)
                retA.setBit(x,y,z, a.bit(x, y, z) ^ (nx1 and x2))
    return retA 

def rc(t):
    if t % 255 == 0:
        return True
    r = BitArray('0b10000000')
    for i in range(1, t%255 + 1):
        r.prepend('0b0')
        r[0] = (r[0] + r[8]) %2
        r[4] = (r[4] + r[8]) %2
        r[5] = (r[5] + r[8]) %2
        r[6] = (r[6] + r[8]) %2
        r = r[:8]
    return r[0]

def iota(a, ir):
    retA = a.copy()
    RC = BitArray(a.w)
    for j in range(int(log(a.w, 2))+1):
        RC[2**j-1] = rc(j+7*ir)
    for z in range(a.w):
        retA.setBit(0,0,z, retA.bit(0,0,z) ^ RC[z])
    return retA
