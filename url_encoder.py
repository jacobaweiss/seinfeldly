def seinfeld_lexicon():
    with open('episodes.txt') as f:
        content = f.read().splitlines()
    return content

ALPHABET = seinfeld_lexicon()
BASE = len(ALPHABET)

def decode(id):
    i = 0
    for c in id.split('-'):
        i = i * BASE + ALPHABET.index(c)
    return i

def encode(n):
    digits = []

    while n > 0:
        remainder = n % BASE
        digits.append(remainder)
        n = n / BASE

    return '-'.join([ALPHABET[n] for n in digits[::-1]])
