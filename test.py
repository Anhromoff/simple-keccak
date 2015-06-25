from StateArray import *

#50 bits
initialstate = BitArray('0x1bcd3842bd2ddc23')
initialstate = initialstate[:50]

a = StateArray(initialstate)
theta(a)

