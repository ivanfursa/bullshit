import random
import sys


def put_to_pile(table, plays):
    ''' A hand passes some (1-4) cards to the pile.
        Returns updated pile. '''
    passing = []
    cards_num = random.randint(1, min(4, len(table[plays])))
    for num in range(cards_num):
        card = random.randint(0, len(table[plays]) - 1)
        passing.append(table[plays][card])
        del table[plays][card]
    passing
    return passing

def is_empty(table, plays):
    ''' Checks if the hand played has become empty.
        Returns True / False. '''
    if len(table[plays]) == 0:
        return True
    else:
        return False

def next_hand(plays, table):
    ''' Updates the hand that goes next. '''
    if plays != len(table)-1:
        plays += 1
    else:
        plays = 0
    return plays

def printing(table, pile):
    ''' Prints the results of the turn:
        what cards are in each hand and in the pile. '''
    for hand in range(len(table)):
        print("Hand", hand+1, table[hand])
    print('pile', pile, '\n')

def carry(table, pile, plays, claimed_passing):
    ''' Carries cards from the pile to either a caller or a playing hand. 
        Caller must not be the playing hand.
        Announces the caller and callee though print(). 
        Returns a transformed table state and a next player identifier. '''
    caller = plays
    while caller == plays:
        caller = random.randint(0, len(table)-1)
    print("Hand", str(caller+1), "calls on hand", str(plays+1))
    
    if claimed_passing == pile[-len(claimed_passing):]:
        carry_to = caller
    else:
        carry_to = plays
    table[carry_to] += pile
    
    if carry_to == plays:
        return table, caller
    elif carry_to == caller:
        return table, plays
    
def set_carry_turn():
    ''' Used for randomizing carry.'''
    carry_turn = random.randint(1, 5)
    return carry_turn

def name_cards(plays, card_values, passing):
    ''' A hand announces which cards it has put into the pile. '''
    num = len(passing)
    # Value of the cards.
    value = card_values[ random.randint(0, len(card_values)-1) ]
    # Making a list of cards a hand said it has put.
    claimed_passing = []
    for i in range(num):
        claimed_passing += [value]
        
    print("Hand", str(plays+1), "plays", str(num), str(value) + "'s")
    return claimed_passing

def initialize_hands(card_values, num_players):
    ''' Depending on a list possible card values and number of players
        creates an initial list of cards for each hand (player) and
        adds them to a list called 'table'. 
        Returns table. '''
    # Get a shuffled deck.
    all_cards = card_values * 4
    deck = random.sample(all_cards, k=len(all_cards))
    
    # Create lists for each hand in put them in list 'table'.
    table = []
    for hand in range(num_players):
        table += [[]]
    
    # Hand-out the cards.
    hand = 0
    while len(deck) != 0:
        table[hand] += deck[0]
        del deck[0]
        
        hand += 1
        if hand == len(table):
            hand = 0
    return table

def check_number_of_cards(table, pile, card_values):
    ''' Make sure the number of cards in the game stays the same. '''
    cards_in_hands = 0
    for hand in table:
        cards_in_hands += len(hand)
    total_cards = len(card_values) * 4
    assert cards_in_hands + len(pile) == total_cards

def get_number_of_players():
    ''' Takes a user input in a form of an integer.
        Checks the number and returns if appropriate. '''
        
    num_players = ''
    while type(num_players) != int:
        try:
            num_players = int(input("Type-in the number of players (2-52): "))
        except ValueError:
            print("Input integers only\n")
    
    if type(num_players) == int and (num_players < 2 or num_players > 52):
        print("Number of players out of range\n")
        num_players = get_number_of_players()
        
    print("")
    return num_players
    
def get_possible_card_values(num_players):
    ''' Takes a user input in a form of an integer.
        Returns a list of possible card values. '''
    all_possible = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    
    print("Type-in the number of card values possible in this game. \
        \nEx.\tif you type '2' (min), possible cards values are 2 and 3 \
        \n\tif you type '13' (max), cards values are from 2 to A. \
        \nIn this game, a standard 52-cards deck is used: \
        \ni.e. no Jokers, possible values are from 2 to A. \
        \nA minimum number you can input depends on a number of players.")
        
    num_values = ''
    while type(num_values) != int:
        try:
            num_values = int(input("Number of possible card values: "))
        except ValueError:
            print("Input integers only\n")
        
        if type(num_values) == int:
            if num_values*4 < num_players:
                print("Too few card values for the game with that many players\n")
                num_values = ''
            elif num_values < 2 or num_values > 13:
                print("Number out of range (2-13)\n")
                num_values = ''
    
    card_values = all_possible[:num_values]
    
    print("")
    return card_values
        
def game_loop():
    ''' Main function of the game.
        The game ends as soon as one hand is empty. '''
    
    # You can change these two variables.
    num_players = get_number_of_players()
    card_values = get_possible_card_values(num_players)
    table = initialize_hands(card_values, num_players)
    
    pile = []
    # 'plays' identifies whose turn it currently is (who plays now).
    plays = 0
    # Turn counter 'turn' controls when calling (carry) happens
    # i.e. when one hand calls on the previously played hand.
    turn = 0
    empty = False
    
    # Print the initial state of the table.
    printing(table, pile)
    
    while not empty:
        # Make sure the number of cards in the game stays the same.
        check_number_of_cards(table, pile, card_values)

        turn += 1
        if pile == []:
            carry_turn = set_carry_turn()
        
        passing = put_to_pile(table, plays)
        claimed_passing = name_cards(plays, card_values, passing)
        pile += passing
        
        if turn == carry_turn:
            table, plays_next = carry(table, pile, plays, claimed_passing)
            turn = 0
            pile = []
        
        # Print the results of the turn.
        printing(table, pile)
        
        empty = is_empty(table, plays)
        if not empty:
            if turn == 0:
                # Next player picked as a result of carry.
                plays = plays_next
            else:
                plays = next_hand(plays, table)
        elif empty and len(pile) > 0:
            # Must call on (check) the empty hand at last.
            # But it could've been already called this turn,
            # therefore check: (len(pile)>0).
            table, plays_next = carry(table, pile, plays, claimed_passing)
            turn = 0
            pile = []
            plays = plays_next
            
            # Print the result of this calling.
            printing(table, pile)
            empty = is_empty(table, plays)
            
    print("The winner is hand " + str(plays+1) + "!")

game_loop()
