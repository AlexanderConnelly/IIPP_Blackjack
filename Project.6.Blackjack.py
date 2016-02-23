# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_SIZE_GAME = (125, 166)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 500
bet=100
in_session=False
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE_GAME)
        
# define hand class


class Hand:
    def __init__(self,is_dealer):
        self.is_dealer=is_dealer
        self.hand=[]
        self.value=0
    def __str__(self):
        return str(self.hand)

    def add_card(self, card):
        self.hand.append(card)
        
        return self.hand

    def get_value(self):
        self.value=0
        ace11=0
        for c in range(0,len(self.hand)):
            
            card=self.hand[c]
            card_value=VALUES[card[1]]
            # add higher ace value if under 11
            
            if card_value==1 and self.value<11:
                self.value+=11
                ace11+=1
            ##add lower ace value if above 11
            elif card_value==1 and self.value>=11:
                self.value+=1
            else:
                self.value+=card_value
            #test if over 21 and have aces at value 11
            if self.value>21 and ace11>0:
                self.value-=10
                ace11-=1
        return self.value
                
                
    def draw(self, canvas, pos):
        if self.is_dealer==True and in_play==True:
            
            card_loc=(100,pos)
            current=self.hand[0]
            suit=current[0]
            rank=current[1]
            card=Card(suit,rank)
            card.draw(canvas, card_loc)
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [CARD_BACK_CENTER[0]+150, pos + CARD_BACK_CENTER[1]], CARD_SIZE_GAME)
                
        else:
            for c in range(0,len(self.hand)):
                card_loc=(100+50*c,pos)
                current=self.hand[c]
                suit=current[0]
                rank=current[1]
                card=Card(suit,rank)
                card.draw(canvas, card_loc)
        
        
# define deck class 
class Deck:
    def __init__(self):
        create_deck=[]
        
        for x in range(0,4):
            for y in range(0,13):
                create_deck.append((SUITS[x],RANKS[y]))
        self.deck=create_deck
        self.deck_pos=0

    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck
    def deal_card(self):
        self.card_delt=self.deck[self.deck_pos]
        if self.deck_pos==len(self.deck)-1:
            print("End of Deck, Shuffling Deck")
            self.shuffle()
            self.deck_pos=0
        else:
            self.deck_pos+=1
        return self.card_delt
    def __str__(self):
        return str(self.deck)

Deck1=Deck()
Deck1.shuffle()

#define event handlers for buttons
def deal():
    global outcome, in_play,player_hand,dealer_hand,bet,score,in_session
    outcome = "New Game, Place Your Bets, Hit or Stay?"
    if in_play==True and in_session==True:
        outcome="Quit Hand Early! You Lost! New Deal?"
        score-=bet
        
        
    in_play = True
    in_session=False
    player_hand=Hand(False)
    dealer_hand=Hand(True)
    
    player_hand.add_card(Deck1.deal_card())
    player_hand.add_card(Deck1.deal_card())
    
    dealer_hand.add_card(Deck1.deal_card())
    dealer_hand.add_card(Deck1.deal_card())

def hit():
    global outcome,in_play,in_session
    in_session=True
    if in_play==True:
        outcome="Player Hits, Hit Again, Or Stay?"
        player_hand.add_card(Deck1.deal_card())	
        if player_hand.get_value()>21:
            win_loose()
       
def stand():
    global outcome,in_play,in_session
    in_session=True
    if in_play==True:
        outcome="Player Stays"
        win_loose()
def win_loose():
    global outcome,in_play,score,bet
    in_play=False
    
    while dealer_hand.get_value()<17:
        dealer_hand.add_card(Deck1.deal_card())
    if player_hand.get_value()>21:
        outcome="Player Looses! New Deal?!"
        score -= bet
    elif dealer_hand.get_value()>21:
        outcome="Dealer Busts! You WIN!!! New Deal!?"
        score += bet
    elif dealer_hand.get_value()>=player_hand.get_value():
        outcome="Dealer Wins! New Deal?!"
        score -= bet
    elif dealer_hand.get_value()<player_hand.get_value():
        outcome="You WIN!!! New Deal?!"
        score += bet
def bet_handler(bet_number):
    global bet
    if bet_number>=100:
        bet=int(bet_number)
# draw handler    
def draw(canvas):
    global outcome,score,in_play
    # test to make sure that card.draw works, replace with your code below
    #Draw Title:
    canvas.draw_text("!!!Blackjack!!!", (0,75), 100, 'yellow')
    #draw player and dealer hand text:
    canvas.draw_text("Player Hand: ("+str(player_hand.get_value())+") "+outcome, (5,400), 25, 'yellow')
    if in_play==True:
        canvas.draw_text("Dealer Hand:", (5,175), 28, 'yellow')
    else:
        canvas.draw_text("Dealer Hand: ("+str(dealer_hand.get_value())+")", (5,175), 28, 'yellow')
    ##Draw Hands:
    player_hand.draw(canvas,450)
    dealer_hand.draw(canvas,230)
    ##Draw Score:
    canvas.draw_text("Money Left= $"+str(score)+" Minimum Bet = $100", (5,125), 28, 'yellow')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_input("Bet Value (Integer + Enter)", bet_handler, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric