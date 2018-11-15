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

def printing(hand_1, hand_2, hand_3, pile):
    ''' Prints the results of the turn. '''
    print('1', hand_1)
    print('2', hand_2)
    print('3', hand_3)
    print('pile', pile, '\n')

def carry(table, pile, plays, caller):
    ''' Carries cards from the pile to either a caller or a playing hand. 
        Returns a transformed table. '''
    carry_to = random.choice([plays, caller])
    table[carry_to] += pile
    return table
    
def set_carry_turn():
    ''' Used for randomizing carry.'''
    carry_turn = random.randint(1, 5)
    return carry_turn
    
def update_turn(turn):
    ''' Returns incremented turn. '''
    turn += 1
    return turn

def name_cards(plays, all_cards, passing):
    ''' A hand says which cards it has put into the pile. '''
    num = len(passing)
    value = all_cards[ random.randint(0, len(all_cards)-1) ]
    print("Hand", str(plays+1), "plays", str(num), str(value) + "'s")
    # return num, value

def who_calls(table, plays):
    ''' Identifies a hand that calls a playing hand.
        Caller must not be the playing hand. 
        Announces the caller and callee. '''
    caller = plays
    while caller == plays:
        caller = random.randint(0, len(table)-1)
    print("Hand", str(caller+1), "calls on hand", str(plays+1))
    return caller

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
    
    while not empty:
        assert (len(hand_1) + len(hand_2) + len(hand_3) + len(pile)) == 20
        turn = update_turn(turn)
        if pile == []:
            carry_turn = set_carry_turn()
        passing = put_to_pile(table, plays)
        name_cards(plays, all_cards, passing)
        pile += passing
        if turn == carry_turn:
            caller = who_calls(table, plays)
            table = carry(table, pile, plays, caller)
            turn = 0
            pile = []
        printing(hand_1, hand_2, hand_3, pile)
        empty = is_empty(table, plays)
        if not empty:
            plays = next_hand(plays, table)
    print("The winner is hand " + str(plays+1) + "!")

game_loop()
