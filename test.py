from StateArray import *
import unittest
import pdb
import itertools

#50 bits
initialstate = BitArray('0x1bcd3842bd2ddc23')
initialstate = initialstate[:50]


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

        x, y, offset = 3, 2, 153
        for z in range(at.w):
            self.assertEqual(at.bit(x,y,z), a.bit(x,y,(z+offset)%at.w))

        x, y, offset = 4, 1, 276
        for z in range(at.w):
            self.assertEqual(at.bit(x,y,z), a.bit(x,y,(z+offset)%at.w))

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

if __name__ == '__main__':
    unittest.main()
