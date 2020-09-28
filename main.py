
import pygame
import random

from collections import namedtuple

#global variables
global deck, hand

# Initializing PyGame
pygame.init()


# COLOR Definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (110, 110, 110)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 120, 0)
RED = (255, 0, 0)
LIGHT_RED = (120, 0, 0)

# Font Definitions
small_font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 50)


# Setting up the screen, background
# WINDOW SIZE
WIDTH = 1600
HEIGHT = 900

# Margins
MARGIN_LEFT = 20
MARGIN_TOP = 150
scaleFactor = 1.4
card_width = int(360 / scaleFactor)
card_height = int(540 / scaleFactor)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(GRAY)
# Setting up caption
pygame.display.set_caption("Jacks or Better Poker")
# Loading image for the icon
icon = pygame.image.load('icon.png')
# Setting the game icon
pygame.display.set_icon(icon)



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


def create_deck():
    deck = []
    # Loop for every type of suit
    for suitX in suit:

        # Loop for every type of card in a suit
        for card in face:
            # Adding the card to the deck
            deck.append(Card(card, suitX))

    return deck

def deal_hand(deck):
    hand=[]
    for x in range(1,6):
        # Choose the card from the deck
        current_card = random.choice(deck)
        hand.append((current_card))
        # Remove the card from the deck
        deck.remove(current_card)
    return (hand)

def renderHand(hand):
    offset = 0
    MARGIN_LEFT = 30
    for card in hand:
        image = pygame.image.load('PlayingCards/' + card.face + card.suit + '.png')
        image_scaled = pygame.transform.scale(image, (card_width,card_height))
        screen.blit(image_scaled, (MARGIN_LEFT + offset, MARGIN_TOP))
        offset += 320
        MARGIN_LEFT= 0




def draw(choice):
    if choice[1] == "hold":
        current_card = random.choice(deck)
        hand.append((current_card))
        # Remove the card from the deck
        deck.remove(current_card)


def set_buttons():
    #Setting up buttons on screen
    screen.blit(button1, button1_rect)
    screen.blit(button2, button2_rect)
    screen.blit(button3, button3_rect)
    screen.blit(button4, button4_rect)
    screen.blit(button5, button5_rect)



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


#Deal the hand

deck = create_deck()

hand = deal_hand(deck)

renderHand(hand)

#clear the choices
choice = ["draw", "draw", "draw", "draw", "draw"]


# Create Buttons
buttonMargin = 20
buttonSpacing = (buttonMargin + (card_width))
button1 = large_font.render("Hold", True, WHITE)
button1_rect = button1.get_rect()
button1_rect.center = (buttonSpacing/2, 600)

button2 = large_font.render("Hold", True, WHITE)
button2_rect = button2.get_rect()
button2_rect.center = (buttonSpacing*1.5, 600)

button3 = large_font.render("Hold", True, WHITE)
button3_rect = button3.get_rect()
button3_rect.center = (buttonSpacing*2.5, 600)

button4 = large_font.render("Hold", True, WHITE)
button4_rect = button4.get_rect()
button4_rect.center = (buttonSpacing*3.5, 600)

button5 = large_font.render("Hold", True, WHITE)
button5_rect = button5.get_rect()
button5_rect.center = (buttonSpacing*4.5, 600)




# The GAME LOOP
while True:

    # Loop events occuring inside the game window
    for event in pygame.event.get():


        # set up buttons
        set_buttons()

        # Qutting event
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #determine if key was clicked (1-5)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                button1 = large_font.render("Hold", True, RED)
                choice[0] = "hold"
            elif event.key == pygame.K_2:
                button2 = large_font.render("Hold", True, RED)
                choice[1] = "hold"
            elif event.key == pygame.K_SPACE:
                if choice[0] == "hold":
                    newCard = random.choice(deck)
                    hand[0] = newCard
                    deck.remove(newCard)
                if choice[1] == "hold":
                    newCard = random.choice(deck)
                    hand[1] = newCard
                    deck.remove(newCard)
                print (choice)
                print (hand)
                renderHand(hand)
                pygame.display.update()
                r = rank(hand)
                handRank = r[0]
                print("%-18s %-15s %s" % ("HAND", "CATEGORY", "TIE-BREAKER"))
                # for cards in hand:
                #     r = rank(cards)
                print("%-18r %-15s %r" % (hand, r[0], r[1]))
                pygame.draw.rect(screen, WHITE, [270, 40, 255, 90],2)
                score_text = small_font.render("Hand Rank = " + handRank, True, BLACK)
                score_text_rect = score_text.get_rect()
                score_text_rect.center = (WIDTH//2, 85)
                screen.blit(score_text, score_text_rect)


    # Update the display after each game loop
    pygame.display.update()
