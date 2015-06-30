from StateArray import *
from math import log

# Define uma rodada do Keccak. Conforme pagina 16 da FIPS-202
def Rnd(A, ir):
    return iota(chi(pi(ro(theta(A)))),ir)

# Classe que define uma instancia de Keccak-p
# Ela pode ser construida passando os parametros b e nr,
# e chamada com a string S (de tamanho b), conforme descrito
# na pagina 16 da FIPS-202.
# Por exemplo, Keccak_p(1600, 24)(s)
class Keccak_p:
    b = 0
    nr = 0
    def __init__(self, b, nr):
        self.b = b
        self.nr = nr
    def __call__(self, s):
        assert len(s) == self.b
	#passo 1
        a = StateArray(s)
        l = int(log(a.w,2))
        i = 0
	#passo 2
        for ir in range(2*l+12-self.nr, 2*l+12):
            a = Rnd(a, ir)
	#passo 3 e 4
        return a.bits

# Definicao de Keccak_f, que gera uma instancia de 
# Keccak_p onde nr = 12+2*l
def Keccak_f(b):
    assert b in [25, 50, 100, 200, 400, 8000, 1600]
    w = b/25
    l = int(log(w,2)) 
    return Keccak_p(b, 12+2*l)

# Definicao da esponja, conforme o algoritmo 8 da FIPS-202
def Sponge(f, pad, r):
    def s(M, d):
        p = BitArray(M)
        byte = []
        # Essa transformacao se faz necessaria, pois dado o byte
        # 0b10101111, numa estrutura do Python BitArray, esse byte
        # tera os indices:
        # [0] [1] [2] [3] [4] [5] [6] [7]
        #  1   0   1   0   1   1   1   1
        # E na especificao do NIST, os algoritmos esperam que o indice
        # [0] seja o bit menos significativo. Entao invertemos os bytes
        trail = BitArray()
        if len(p) % 8 != 0:
            parts = int(len(p)/8)
            trail = p[parts*8:]
        for i in range(int(len(p)/8)):
            b = p[i*8:(i+1)*8]
            b.reverse()
            byte.append(b)
        byte.append(trail)
        p = BitArray().join(byte)
        
        # Passo 1
        p.append(pad(r, len(p)))
        # Passo 2
	assert(len(p)%r == 0)	
	n = len(p)/r
        # Passo 3
        c = f.b-r
        
        # Passo 4
        parts = []
        for i in range(n):
            parts.append(p[i*r: (i+1)*r])

        # Passo 5
        s = BitArray(f.b)
        # Passo 6
        for part in parts:
            s = s ^ (part + BitArray(c))
            s = f(s)
        # Passos 8, 9, 10
        Z = s[:r]
        while d > len(Z):
            Z += f(S)
        Z = Z[:d]
        
        # Analogamente ao que foi feito antes, precisamos inverter
        # os bytes novamente para retornar a saida correta
        byte = []
        for i in range(int(len(Z)/8)):
            b = Z[i*8:(i+1)*8]
            b.reverse()
            byte.append(b)
        Z = BitArray().join(byte)
        return Z

    return s

# Funcao de padding conforme algoritmo 9
def pad101(x, m):
    j = (-m-2)%x
    return BitArray('0b1') + BitArray(j) + BitArray('0b1')

# Funcao Keccak conforme definido na pagina 19 do FIPS-202
def Keccak(c):
    return Sponge(Keccak_p(1600,24), pad101, 1600-c)

# Definicao das funcoes SHA conforme item 6.1 do FIPS-202
def SHA3_224(M):
    return Keccak(448)(BitArray(bytes=M)+BitArray("0b01"), 224)

def SHA3_256(M):
    return Keccak(512)(BitArray(bytes=M)+BitArray("0b01"), 256)

def SHA3_384(M):
    return Keccak(768)(BitArray(bytes=M)+BitArray("0b01"), 384)

def SHA3_512(M):
    return Keccak(1024)(BitArray(bytes=M)+BitArray("0b01"), 512)
