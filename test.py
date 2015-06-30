from StateArray import *
from Keccak import *
import unittest
import pdb
import itertools

#50 bits
initialstate = BitArray('0x1bcd3842bd2ddc23')*20
initialstate = initialstate[:200]
        
#Taken from:
# http://keccak.noekeon.org/specs_summary.html
RC = []
RC.append('0x0000000000000001')  
RC.append('0x0000000000008082')  
RC.append('0x800000000000808A')  
RC.append('0x8000000080008000')  
RC.append('0x000000000000808B')  
RC.append('0x0000000080000001')  
RC.append('0x8000000080008081')  
RC.append('0x8000000000008009')  
RC.append('0x000000000000008A')  
RC.append('0x0000000000000088')  
RC.append('0x0000000080008009')  
RC.append('0x000000008000000A')  
RC.append('0x000000008000808B') 
RC.append('0x800000000000008B') 
RC.append('0x8000000000008089') 
RC.append('0x8000000000008003') 
RC.append('0x8000000000008002') 
RC.append('0x8000000000000080') 
RC.append('0x000000000000800A') 
RC.append('0x800000008000000A') 
RC.append('0x8000000080008081') 
RC.append('0x8000000000008080') 
RC.append('0x0000000080000001') 
RC.append('0x8000000080008008') 


class TestStateArray(unittest.TestCase):

    def test_theta(self):
        a = StateArray(initialstate)
        at = theta(a)
        x = 3
        y = 2
        z = 1
        c1 = a.bit(x-1,0,z) \
           ^ a.bit(x-1,1,z) \
           ^ a.bit(x-1,2,z) \
           ^ a.bit(x-1,3,z) \
           ^ a.bit(x-1,4,z) 
        c2 = a.bit(x+1,0,z-1) \
           ^ a.bit(x+1,1,z-1) \
           ^ a.bit(x+1,2,z-1) \
           ^ a.bit(x+1,3,z-1) \
           ^ a.bit(x+1,4,z-1) 
        expected = a.bit(x,y,z) ^ c1 ^ c2
        self.assertEqual(at.bit(x,y,z), expected)

    def test_ro(self):
        a = StateArray(initialstate)
        at = ro(a)

        offsets = [[0, 36, 3, 105, 210],
                   [1, 300, 10, 45, 66],
                   [190, 6, 171, 15, 253],
                   [28, 55, 153, 21, 120],
                   [91, 276, 231, 136, 78]]

        for x in range(5):
            for y in range(5):
                offset = offsets[x][y]
                for z in range(a.w):
                    self.assertEqual(a.bit(x,y,z), at.bit(x,y,(z+offset)%at.w))

    def test_pi(self):
        a = StateArray(initialstate)
        at = pi(a)
        for x, y in itertools.product(range(5), range(5)):
            self.assertEqual(at.lane(x,y), a.lane((x+3*y)%5, x))

    def test_chi(self):
        a = StateArray(initialstate)
        at = chi(a)
        
        #Checking x = 0 for every row
        for y, z in itertools.product(range(5), range(a.w)):
            val = (not a.bit(1,y,z)) and (a.bit(2,y,z))
            self.assertEqual(at.bit(0,y,z), a.bit(0,y,z) ^ val)

    def test_rc(self):
        self.assertEqual(len(RC), 24)
    
        for ir in range(24):
            rcarray = BitArray(64)
            for j in range(7):
                rcarray[2**j-1] = rc(j+7*ir)
            rcarray.reverse()
            self.assertEqual(rcarray, RC[ir])
    
    def test_iota(self):
        a = StateArray(initialstate)
        
        #iota should NOT affect any lane beyond 0,0
        at = iota(a,0)
        for x, y in itertools.product(range(5), range(5)):
            if x != 0 or y != 0:
                self.assertEqual(at.lane(x,y), a.lane(x,y))

        for ir in range(24):
            at = iota(a, ir)
            truncRC = BitArray(RC[ir])
            truncRC.reverse()
            truncRC = truncRC[:a.w]
            self.assertEqual(at.lane(0,0), a.lane(0,0) ^ truncRC)
    
class TestKeccack(unittest.TestCase):

    def test_pad101(self):
        for x in range(1, 20):
            for m in range(100):
                pad = pad101(x,m)
                self.assertEqual((m+len(pad))%x, 0)

    def test_null_string(self):
        k244 = Keccak(448)("", 224)
        self.assertEqual(k244, "0xf71837502ba8e10837bdd8d365adb85591895602fc552b48b7390abd")
        sha3foobar = Keccak(768)(BitArray(bytes="foobar") + BitArray('0b01'), 384)
        self.assertEqual(sha3foobar, "0x0fa8abfbdaf924ad307b74dd2ed183b9a4a398891a2f6bac8fd2db7041b77f068580f9c6c66f699b496c2da1cbcc7ed8")
        
        k256 = Keccak(512)("", 256)
        self.assertEqual(k256, "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad804"
                             + "5d85a470")
        
        k384 = Keccak(768)("", 384)
        self.assertEqual(k384, "0x2c23146a63a29acf99e73b88f8c24eaa7dc60aa771780ccc006afbfa"
                             + "8fe2479b2dd2b21362337441ac12b515911957ff") 
        
        k512 = Keccak(1024)("", 512)
        self.assertEqual(k512, "0x0eab42de4c3ceb9235fc91acffe746b29c29a8c366b7c60e4e67c466"
                             + "f36a4304c00fa9caf9d87976ba469bcbe06713b435f091ef2769fb160c"
                             + "dab33d3670680e")

    
if __name__ == '__main__':
    unittest.main()
