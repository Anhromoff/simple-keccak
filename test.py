from StateArray import *
import unittest
import pdb

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

if __name__ == '__main__':
    unittest.main()
