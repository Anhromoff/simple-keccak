from bitstring import BitArray

class StateArray:
    bits = 0
    w = 0
    def __init__(self, bits):
        self.bits = BitArray(bits)
        assert len(self.bits) in [25, 50, 100, 200, 400, 800, 1600]
        self.w = len(self.bits)/25
    
    def bit(self, x, y, z):
        assert x < 5
        assert y < 5
        assert z < self.w
        return self.bits[self.w*(5*y+z) + z]
    
    def setBit(self, x, y, z, val):
        assert x < 5
        assert y < 5
        assert z < self.w
        self.bits[self.w*(5*y+z) + z] = val

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
