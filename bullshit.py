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

def name_cards(plays, all_cards, passing):
    ''' A hand announces which cards it has put into the pile. '''
    num = len(passing)
    # Value of the cards.
    value = all_cards[ random.randint(0, len(all_cards)-1) ]
    # Making a list of cards a hand said it has put.
    claimed_passing = []
    for i in range(num):
        claimed_passing += [value]
        
    print("Hand", str(plays+1), "plays", str(num), str(value) + "'s")
    return claimed_passing
    
    

def game_loop():
    ''' Main function of the game.
        The game ends as soon as one hand is empty. '''
    
    all_cards = [
        '2','2','2','2',
        '3','3','3','3',
        '4','4','4','4',
        '5','5','5','5',
        '6','6','6','6',
        ]
        
    hand_1 = ['x', 'x', 'x', 'x', 'x', 'x', 'x']
    hand_2 = ['2', '3', '3', '4', '4', '5', '6']
    hand_3 = ['x', 'x', 'x', 'x', 'x', 'x']
    
    pile = []
    
    table = [hand_1, hand_2, hand_3]
    plays = 0
    turn = 0
    empty = False
    
    # Print the initial state of the table.
    printing(table, pile)
    
    while not empty:
        # Check the number of cards in the game stays the same.
        assert (len(hand_1) + len(hand_2) + len(hand_3) + len(pile)) == 20
        
        # Turn counter is coordinate when calling (carry) happens
        # i.e. when one hand calls on the previously played hand.
        turn += 1
        if pile == []:
            carry_turn = set_carry_turn()
        
        passing = put_to_pile(table, plays)
        claimed_passing = name_cards(plays, all_cards, passing)
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
