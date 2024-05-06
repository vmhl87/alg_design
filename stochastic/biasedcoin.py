import random
def biased_flip(p):
    return random.random() < p

# previously rolled heads, tails, probability
p_heads, p_tails, p_prob = 0, 0, 0

def compounding_biased_flip(p):
    global p_heads, p_tails, p_prob

    # update running sums when probability changes
    if p_prob != p:
        p_heads, p_tails = 0, 0
        p_prob = p

    # running average if true or false is chosen
    ift = (p_heads + 1) / (p_heads + p_tails + 1)
    iff = p_heads / (p_heads + p_tails + 1)

    # compare which is closer to target probability
    if abs(ift - p) < abs(iff - p):
        p_heads += 1
        return True
    else:
        p_tails += 1
        return False

def test_bias(p, flip=biased_flip, itr=1000):
    return sum([1 if flip(p) else 0 for _ in range(itr)])/itr
