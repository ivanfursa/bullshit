from random import randint
import sys



def update_pile(table, plays, pile):
    ''' A hand passes some (1-4) cards to the pile.
        Returns updated pile. '''
    passing = []
    cards_num = randint(1, min(4, len(table[plays])))
    for num in range(cards_num):
        card = randint(0, len(table[plays]) - 1)
        passing.append(table[plays][card])
        del table[plays][card]
    pile += passing
    return pile

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

def winner(plays):
    ''' Announes a winner hand. '''
    print("The winner is hand " + str(plays+1) + "!")

def carry(table, pile, plays):
    ''' Carries cards from the pile to a random hand at some target turn. 
        Returns a transformed hand (table[plays]). '''
    table[plays] += pile
    return table[plays]
    
def set_carry_turn():
    ''' Used for randomizing carry.'''
    carry_turn = randint(1, 5)
    return carry_turn
    
def update_turn(turn):
    ''' Returns incremented turn. '''
    turn += 1
    return turn

def game_loop():
    ''' Main function of the game.
        The game ends as soon as one hand is empty. '''
    
    # Testing on a set of cards from 2 to 6 including

    hand_1 = ['x', 'x', 'x', 'x', 'x', 'x', 'x']
    hand_2 = ['2', '3', '3', '4', '4', '5', '6']
    hand_3 = ['x', 'x', 'x', 'x', 'x', 'x']
    
    pile = []
    
    assert (len(hand_1) + len(hand_2) + len(hand_3)) % 4 == 0
    
    table = [hand_1, hand_2, hand_3]
    plays = 0
    turn = 0
    empty = False
    
    while not empty:
        turn = update_turn(turn)
        if pile == []:
            carry_turn = set_carry_turn()
        pile = update_pile(table, plays, pile)
        if turn == carry_turn:
            table[plays] = carry(table, pile, plays)
            turn = 0
            pile = []
        printing(hand_1, hand_2, hand_3, pile)
        empty = is_empty(table, plays)
        if not empty:
            plays = next_hand(plays, table)
    winner(plays)

game_loop()
