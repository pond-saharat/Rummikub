class Deck:
    def __init__(self):
        cards_pool = NUM_OF_SAME_CARD * [Card(colour, i) for colour in NOW_COLOURS for i in range(1, NUM_OF_CARDS_EACH_COLOUR+1)]
        cards_pool += NUM_OF_WILDCARDS * [Card.wildcard]
        random.shuffle(cards_pool)
        self.cards_pool = cards_pool