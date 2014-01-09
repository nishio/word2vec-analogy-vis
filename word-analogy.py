"""
port of word-analogy.c
"""
import argparse
import struct
from math import sqrt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--test', action='store_true', help='use small data and do regression test')
args = parser.parse_args()

N = 40

f = file('vectors.bin', 'rb')
words, size = map(int, f.readline().split())
if args.test: words = 50  # small data

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
    M[b] = np.zeros(size)
    for a in range(size):
        M[b][a] = struct.unpack('f', f.read(FLOAT_SIZE))[0]

    mag_vec = np.linalg.norm(M[b], 2)
    M[b] /= mag_vec  # normalize vector
    assert f.read(1) == '\n'  # strip newline

f.close()

while True:
    bestd = [0] * N
    bestw = [None] * N
    if not args.test:
        st1 = raw_input("Enter three words (EXIT to break): ")
        if st1 == 'EXIT': break
    else:
        st1 = 'a the of'

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

    vec = M[bi[1]] - M[bi[0]] + M[bi[2]]
    mag_vec = np.linalg.norm(vec, 2)
    vec /= mag_vec  # normalize vector

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

    if args.test:
        expected = [(0.43589739071989975, 'its'), (0.40574892064435714, 'in'), (0.37634475225790609, 'and'), (0.3357552560549707, 's'), (0.33309901380186097, 'from')]
        if ranking[:5] == expected:
            print 'ok.'
        else:
            print ranking[:5]
            print expected
            print 'ng.'
        break
