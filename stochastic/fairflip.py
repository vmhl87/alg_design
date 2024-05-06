from biasedcoin import biased_flip, test_bias

def fair_flip(p=0.83):
    h, t = 0, 0
    while h == t:
        if biased_flip(p): h += 1
        else: t += 1
        if biased_flip(p): t += 1
        else: h += 1
    return h > t
