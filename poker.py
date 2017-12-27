import random, time

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n=5, deck=mydeck):
    '''alternative solution
    deck2 = deck[:]
    random.shuffle(deck2)
    deals = []
    for k in range(numhands):
        deals.append([]) 
    for i in range(n):
        for j in range(numhands):
            deals[j].append(deck2.pop(0))
    return deals
    '''
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(numhands)]


def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    '''alternative solution
    iterable = sorted(iterable, reverse=True, key=key)
    mapped = [(i, hand_rank(i)) for i in iterable]
    winners = []
    for i in mapped:
        if i[1] == mapped[0][1]:
            winners.append(i[0])
        else:
            break
    return winners if len(winners) > 1 else [winners[0]]
    '''
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
    ranks.sort(reverse=True)
    if ranks == [14, 5, 4, 3, 2]:
        return [5, 4, 3, 2, 1]
    return ranks
    
def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # pair
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)
    
def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    '''alternative solution
    out = set()
    for i, item in enumerate(ranks):
        out.add(item + i)
    return len(out) == 1
    '''
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5
    
def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for i in ranks:
        if n == ranks.count(i):
            return i
    
def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    '''alternative solution
    s = set()
    for i in ranks:
        if 2 == ranks.count(i):
            s.add(i)
    if len(s) == 2: return tuple(s)
    '''
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)

def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # => ['6C', '7C', '8C', '9C', 'TC']
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() 
    fh = "TD TC TH 7C 7D".split()
    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert straight(card_ranks(al)) == True 
    print("function 'straight' passes")

    assert flush(sf) == True
    assert flush(fk) == False
    print("function 'flush' passes")
    
    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert card_ranks(['AC', '3D', '4S', 'KH']) == [14, 13, 4, 3]
    print("function 'card_ranks' passes")
    
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    print("function 'kind' passes")
    
    assert two_pair(fkranks) == None
    assert two_pair(tpranks) == (9, 5)
    print("function 'two_pair' passes")
    
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    print("function 'hand_rank' passes")
    
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert poker([sf, sf2, fk, fh]) == [sf, sf2]
    assert poker([sf2, fk, fh]) == [sf2]
    print("function 'poker' passes")    
    
    return "all tests pass"
  
def hand_percentages(n=700*1000):
    start = time.time()
    counts = [0]*9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print("%14s: %6.3f %%") % (i, 100.*counts[i]/n)
    print("Done in", time.time() - start)
    
#print test()
#print deal(2)
#hand_percentages(10000)

