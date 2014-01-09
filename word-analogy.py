"""
port of word-analogy.c
"""
import struct
from math import sqrt
import Queue
N = 40

f = file('vectors.bin', 'rb')
words, size = map(int, f.readline().split())

vocab = [None] * words
M = [None] * words  # matrix
FLOAT_SIZE = struct.calcsize('f')  # == 4

for b in range(words):
    # find word
    c = None
    s = ''
    while True:
        c = f.read(1)
        if c == ' ': break
        s += c
    vocab[b] = s
    M[b] = [None] * size
    mag_vec = 0.0
    for a in range(size):
        M[b][a] = struct.unpack('f', f.read(FLOAT_SIZE))[0]
        mag_vec += M[b][a] * M[b][a]

    mag_vec = sqrt(mag_vec)
    for a in range(size):
        M[b][a] /= mag_vec  # normalize vector

    assert f.read(1) == '\n'  # strip newline

f.close()

while True:
    bestd = [0] * N
    bestw = [None] * N
    st1 = raw_input("Enter three words (EXIT to break): ")
    if st1 == 'EXIT': break

    cn = 0
    b = 0
    c = 0
    st = st1.split()
    cn = len(st)
    if cn < 3:
      print("Only %d words were entered.. three words are needed at the input to perform the calculation" % cn)
      continue

    bi = [None] * 3
    for a in range(cn):
        try:
            b = vocab.index(st[a])
        except:
            b = 0  # not found
        bi[a] = b
        print("\nWord: %s  Position in vocabulary: %d"
              % (st[a], bi[a]))
        if b == 0:
            print("Out of dictionary word!\n")
            break

    if b == 0: continue
    print("\n                                       Word              Distance\n------------------------------------------------------------------------");
    vec = [0] * size
    for a in range(size):
        vec[a] = M[bi[1]][a] - M[bi[0]][a] + M[bi[2]][a]
    mag_vec = 0.0
    for a in range(size):
        mag_vec += vec[a] * vec[a]
    mag_vec = sqrt(mag_vec)
    for a in range(size):
        vec[a] /= mag_vec

    ranking = []
    for c in range(words):
        if c in bi: continue
        dist = 0.0
        for a in range(size):
            dist += vec[a] * M[c][a]

        ranking.append((dist, vocab[c]))
    ranking.sort(reverse=True)
    for a in range(N):
        d, w = ranking[a]
        print("%50s\t\t%f" % (w, d));