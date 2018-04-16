import unittest
from  src.model.cards import *
from  src.view import *

# Tests the cards
class TestCards(unittest.TestCase):

    # tests the card class
    def test_card(self):
        example = Card('1', 'hearts', True)
        self.assertTrue(example.rank == '1')
        self.assertTrue(example.suit == 'hearts')
        self.assertTrue(example.visible)
        example.makeInvisible()
        self.assertFalse(example.visible)
        example.makeVisible()
        self.assertTrue(example.visible)

    # tests the deck class
    def test_deck(self):
        deck = Deck()
        before_shuffle = []
        for card in deck.listOfCards:
            card.makeVisible()
            before_shuffle.append(card)

        deck.shuffle()
        after_shuffle = deck.listOfCards
        
        # theres an extremely low possibility that the deck will be the
        # same after shuffling.
        self.assertFalse(before_shuffle == after_shuffle)
        
    # tests the pile class
    def test_pile(self):
        card1 = Card('1', 'Hearts', True )
        card2 = Card('2', 'Spades', True )
        list_of_cards = [card1, card2]
        pile1 = Pile(list_of_cards)
        pile2 = Pile()
        self.assertTrue(pile1.cards == list_of_cards)
        self.assertTrue(pile2.cards == [])
        self.assertTrue(len(pile1) == 2)
        self.assertTrue(len(pile2) == 0)
        self.assertTrue(pile1.top() == card2)
        self.assertTrue(card1 == pile1[0])

        pile1.giveOneCard(pile2)

        self.assertTrue(len(pile2) == 1)
        pile1.giveOneCard(pile2)
        self.assertTrue(len(pile2) == 2)

        self.assertTrue(pile1.isEmpty())

    
if __name__ == '__main__':
    unittest.main()
