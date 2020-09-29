
import pygame
import random

from collections import namedtuple


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
buttonY = 800


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

# Button class definition
class Button:
    def __init__(self, position, color, value, locationX, locationY):
        self.position = position
        self.color = color
        self.value = value
        self.locationX = locationX
        self.locationY = locationY

    def render_button(self):
        if self.value:
            self.color = RED
        else:
            self.color = WHITE
        button = large_font.render("HOLD", True, self.color)
        button_rect = button.get_rect()
        button_rect.center = (self.locationX, self.locationY)
        screen.blit(button, button_rect)



#Ingredients for creating and ranking cards
suit = 'h d c s'.split()
faces = '2 3 4 5 6 7 8 9 10 j q k a'
lowaces = 'a 2 3 4 5 6 7 8 9 10 j q k'
face = faces.split()
lowace = lowaces.split()

def shuffle_and_deal():

    #create the deck. Creates 52 Card Objects.
    deck = []
    for suitX in suit:
        for card in face:
            # Adding the card to the deck
             deck.append(Card(card, suitX))

    #deal the hand
    hand=[]
    for x in range(1,6):
        # Choose the card from the deck
        current_card = random.choice(deck)
        hand.append((current_card))
        # Remove the card from the deck
        deck.remove(current_card)

    #render the cards on screen
        renderHand(hand)
    #render the buttons
        choices = [False, False, False, False, False]
        set_buttons(choices)

    return  deck, hand, choices

def renderHand(hand):
    offset = 0
    MARGIN_LEFT = 30
    for card in hand:
        image = pygame.image.load('PlayingCards/' + card.face + card.suit + '.png')
        image_scaled = pygame.transform.scale(image, (card_width,card_height))
        screen.blit(image_scaled, (MARGIN_LEFT + offset, MARGIN_TOP))
        offset += 320
        MARGIN_LEFT= 0

def set_buttons(choices):
    pos1 = MARGIN_LEFT + (card_width/2)
    spacing = card_width + 20
    buttons = []
    buttons.append(Button(0,WHITE,choices[0], pos1, buttonY))
    buttons.append(Button(1,WHITE,choices[1],spacing, buttonY))
    buttons.append(Button(2,WHITE,choices[2],spacing*2, buttonY))
    buttons.append(Button(3,WHITE,choices[3],spacing*3, buttonY))
    buttons.append(Button(4,WHITE,choices[4],spacing*4, buttonY))

    for button in buttons:
        button.render_button()

def draw(choices, hand, deck):
    n=0
    for choice in choices:
        if choice == False:
            current_card = random.choice(deck)
            hand[n] = current_card
            deck.remove(current_card)
        n+=1
    return choices, hand, deck





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

newGame = True

# The GAME LOOP
while True:

    return_as_tuple = shuffle_and_deal()
    deck = return_as_tuple[0]
    hand = return_as_tuple[1]
    choices = return_as_tuple[2]

    print (hand)
    newGame = False

    while newGame == False:

        # Loop events occuring inside the game window
        for event in pygame.event.get():
            # Qutting event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # determine if key was clicked (1-5)
            # toggle value if keypressed. False = Draw, True = Hold

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choices[0] = not choices[0]
                elif event.key == pygame.K_2:
                    choices[1] = not choices[1]
                elif event.key == pygame.K_3:
                    choices[2] = not choices[2]
                elif event.key == pygame.K_4:
                    choices[3] = not choices[3]
                elif event.key == pygame.K_5:
                    choices[4] = not choices[4]
                elif event.key == pygame.K_SPACE:
                    returnValue = draw(choices, hand, deck)
                    choices = returnValue[0]
                    hand = returnValue[1]
                    deck = returnValue[2]
                    print (choices)
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
                elif event.key == pygame.K_RETURN:
                    screen.fill(GRAY)
                    newGame = True

                set_buttons(choices)





        # Update the display after each game loop
        pygame.display.update()
