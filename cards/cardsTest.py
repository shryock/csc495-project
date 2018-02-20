import cards
import sys

deck = cards.Deck()
deck.shuffle()
howMany = [12, 2]
listOfPiles = deck.distributeCardsToPiles(howMany)
for pile in listOfPiles:
    pile.makeAllCardsVisible()
    print(pile)

listOfPiles[0].giveSetOfCards(5, listOfPiles[1])

print(listOfPiles[0])
print(listOfPiles[1])

for pile in listOfPiles:
    pile.makeAllCardsInvisible()
    print(pile)

listOfPiles[0].giveOneCard(listOfPiles[1])

for pile in listOfPiles:
    pile.makeAllCardsVisible()
    print(pile)
