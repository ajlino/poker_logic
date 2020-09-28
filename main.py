
import pygame
import random

from collections import namedtuple

#This is a test for github

# Margins
MARGIN_LEFT = 20
MARGIN_TOP = 150

# WINDOW SIZE
WIDTH = 800
HEIGHT = 600

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (110, 110, 110)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 120, 0)
RED = (255, 0, 0)
LIGHT_RED = (120, 0, 0)

# Initializing PyGame
pygame.init()

# WINDOW SIZE
WIDTH = 800
HEIGHT = 600

# Setting up the screen and background
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(GRAY)

# Setting up caption
pygame.display.set_caption("Jacks or Better Poker")

# Loading image for the icon
icon = pygame.image.load('icon.png')

# Setting the game icon
pygame.display.set_icon(icon)

# Types of fonts to be used
small_font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 50)




# Card class definition
class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self)

suit = 'h d c s'.split()
# ordered strings of faces
faces = '2 3 4 5 6 7 8 9 10 j q k a'
lowaces = 'a 2 3 4 5 6 7 8 9 10 j q k'
# faces as lists
face = faces.split()
lowace = lowaces.split()


#Create Deck
deck = []
# Loop for every type of suit
for suitX in suit:

    # Loop for every type of card in a suit
    for card in face:
        # Adding the card to the deck
        deck.append(Card(card, suitX))





def straightflush(hand):
    f, fs = ((lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces))
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if (all(card.suit == first.suit for card in rest) and
            ' '.join(card.face for card in ordered) in fs):
        return 'straight-flush', ordered[-1].face
    return False


def fourofakind(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 4:
            allftypes.remove(f)
            return 'four-of-a-kind', [f, allftypes.pop()]
    else:
        return False


def fullhouse(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return 'full-house', [f, allftypes.pop()]
    else:
        return False


def flush(hand):
    allstypes = {s for f, s in hand}
    if len(allstypes) == 1:
        allfaces = [f for f, s in hand]
        return 'flush', sorted(allfaces,
                               key=lambda f: face.index(f),
                               reverse=True)
    return False


def straight(hand):
    f, fs = ((lowace, lowaces) if any(card.face == '2' for card in hand)
             else (face, faces))
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    if ' '.join(card.face for card in ordered) in fs:
        return 'straight', ordered[-1].face
    return False


def threeofakind(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) <= 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return ('three-of-a-kind', [f] +
                    sorted(allftypes,
                           key=lambda f: face.index(f),
                           reverse=True))
    else:
        return False


def twopair(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 2:
        return False
    p0, p1 = pairs
    other = [(allftypes - set(pairs)).pop()]
    return 'two-pair', pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other

def onepairJacks(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if (allfaces.count(f) == 2 and (f=="j" or f=="q" or f=="k" or f=="a"))]
    if len(pairs) != 1:
        return False
    allftypes.remove(pairs[0])
    return 'one-pair JACKS OR Higher Winner', pairs + sorted(allftypes,
                                      key=lambda f: face.index(f),
                                      reverse=True)

def onepair(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if (allfaces.count(f) == 2)]
    if len(pairs) != 1:
        return False
    allftypes.remove(pairs[0])
    return 'one-pair', pairs + sorted(allftypes,
                                      key=lambda f: face.index(f),
                                      reverse=True)


def highcard(hand):
    allfaces = [f for f, s in hand]
    return 'high-card', sorted(allfaces,
                               key=lambda f: face.index(f),
                               reverse=True)


handrankorder = (straightflush, fourofakind, fullhouse,
                 flush, straight, threeofakind,
                 twopair, onepairJacks, onepair, highcard)


def rank(hand):
    # hand = handy(cards)
    for ranker in handrankorder:
        rank = ranker(hand)
        if rank:
            break
    assert rank, "Invalid: Failed to rank cards: %r" % cards
    return rank


# def handy(cards='2♥ 2♦ 2♣ k♣ q♦'):
#     hand = []
#     for card in cards.split():
#         f, s = card[:-1], card[-1]
#         assert f in face, "Invalid: Don't understand card face %r" % f
#         assert s in suit, "Invalid: Don't understand card suit %r" % s
#         hand.append(Card(f, s))
#     assert len(hand) == 5, "Invalid: Must be 5 cards in a hand, not %i" % len(hand)
#     assert len(set(hand)) == 5, "Invalid: All cards in the hand must be unique %r" % cards
#     return hand

#Deal the hand
hand = []
for x in range(1,6):
    # Choose the card from the deck
    current_card = random.choice(deck)
    hand.append((current_card))
    # Remove the card from the deck
    deck.remove(current_card)

# Load the card images
card1 = pygame.image.load('PlayingCards/' + hand[0].face + hand[0].suit + '.png')
card2 = pygame.image.load('PlayingCards/' + hand[1].face + hand[1].suit + '.png')
card3 = pygame.image.load('PlayingCards/' + hand[2].face + hand[2].suit + '.png')
card4 = pygame.image.load('PlayingCards/' + hand[3].face + hand[3].suit + '.png')
card5 = pygame.image.load('PlayingCards/' + hand[4].face + hand[4].suit + '.png')

# scale the images
card1 = pygame.transform.scale(card1, (100,160))
card2 = pygame.transform.scale(card2, (100,160))
card3 = pygame.transform.scale(card3, (100,160))
card4 = pygame.transform.scale(card4, (100,160))
card5 = pygame.transform.scale(card5, (100,160))

# Create Buttons
button1 = large_font.render("Hold", True, WHITE)
button1_rect = button1.get_rect()
button1_rect.center = (70, 400)

button2 = large_font.render("Hold", True, WHITE)
button2_rect = button2.get_rect()
button2_rect.center = (190, 400)

button3 = large_font.render("Hold", True, WHITE)
button3_rect = button3.get_rect()
button3_rect.center = (310, 400)

button4 = large_font.render("Hold", True, WHITE)
button4_rect = button4.get_rect()
button4_rect.center = (430, 400)

button5 = large_font.render("Hold", True, WHITE)
button5_rect = button5.get_rect()
button5_rect.center = (550, 400)

r = rank(hand)

print("%-18s %-15s %s" % ("HAND", "CATEGORY", "TIE-BREAKER"))
# for cards in hand:
#     r = rank(cards)
print("%-18r %-15s %r" % (hand, r[0], r[1]))


# The GAME LOOP
while True:

    # Debugging code
    # hand=[]
    # hand.append(deck[9])
    # hand.append(deck[22])
    # hand.append(deck[2])
    # hand.append(deck[3])
    # hand.append(deck[4])
    # print (hand) # Gives [j♥, j♦, 4♥, 5♥, 6♥]


    # Loop events occuring inside the game window
    for event in pygame.event.get():

        # Qutting event
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    padding = 120

    #Setting up cards on screen
    screen.blit(card1, (MARGIN_LEFT, MARGIN_TOP))
    screen.blit(card2, (MARGIN_LEFT + padding, MARGIN_TOP))
    screen.blit(card3, (MARGIN_LEFT + (padding*2), MARGIN_TOP))
    screen.blit(card4, (MARGIN_LEFT + (padding*3), MARGIN_TOP))
    screen.blit(card5, (MARGIN_LEFT + (padding*4), MARGIN_TOP))

    #Setting up buttons on screen
    screen.blit(button1, button1_rect)
    screen.blit(button2, button2_rect)
    screen.blit(button3, button3_rect)
    screen.blit(button4, button4_rect)
    screen.blit(button5, button5_rect)

    handRank=r[0]

    pygame.draw.rect(screen, WHITE, [270, 40, 255, 90],2)
    score_text = small_font.render("Hand Rank = " + handRank, True, BLACK)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (WIDTH//2, 85)
    screen.blit(score_text, score_text_rect)

    # Update the display after each game loop
    pygame.display.update()
