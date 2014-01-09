"""
port of word-analogy.c
"""
import argparse
import struct
from math import sqrt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--test', action='store_true', help='use small data and do regression test')
parser.add_argument('--vis', action='store_true', help='visualize')
args = parser.parse_args()

def normalize(vec, inplace=False):
    mag_vec = np.linalg.norm(vec, 2)
    if inplace:
        vec /= mag_vec
    else:
        return vec / mag_vec

def add_vis_target(c):
    v = M[c] - M[bi[0]]
    x1 = v.dot(e1)
    x2 = v.dot(e2)
    x1, x2 = x1 - tw * x2, x2 - tw * x1
    if -n1 < x1 < 2 * n1 and -n2 < x2 < 2 * n2:
        vis_target.append((x1, x2, vocab[c]))


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

    normalize(M[b], True)
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
    normalize(vec, True)
    if args.vis:
        d1 = M[bi[1]] - M[bi[0]]
        d2 = M[bi[2]] - M[bi[0]]
        n1 = np.linalg.norm(d1, 2)
        n2 = np.linalg.norm(d2, 2)
        e1 = normalize(d1)
        e2 = normalize(d2)
        tw = e1.dot(e2)
        vis_target = []

    ranking = []
    for c in range(words):
        if c in bi: continue
        dist = vec.dot(M[c])
        ranking.append((dist, vocab[c], c))

    ranking.sort(reverse=True)
    for a in range(N):
        d, w, c = ranking[a]
        print("%50s\t\t%f" % (w, d));
        if args.vis:
            add_vis_target(c)

    if args.vis:
        import matplotlib.pyplot as plt
        for c in bi:
            add_vis_target(c)

        xs, ys, ws = zip(*vis_target)
        ax = plt.figure().add_subplot(111)
        ax.scatter(xs, ys, marker='o')

        for x, y, w in vis_target:
            plt.annotate(
                w, xy = (x, y))

        plt.savefig('vis.png')

    if args.test:
        expected = [(int(x * 10000), y) for (x, y) in
            [(0.43589739071989975, 'its'), (0.40574892064435714, 'in'), (0.37634475225790609, 'and'), (0.3357552560549707, 's'), (0.33309901380186097, 'from')]]
        got = [(int(x * 10000), y) for (x, y, c) in ranking[:5]]
        if got == expected:
            print 'ok.'
        else:
            print got
            print expected
            print 'ng.'
        break
