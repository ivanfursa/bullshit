from random import randint
import sys

total_cards = [
    '2', '2', '2', '2',
    '3', '3', '3', '3',
    '4', '4', '4', '4',
    '5', '5', '5', '5',
    '6', '6', '6', '6',
    ]

hand_1 = ['x', 'x', 'x', 'x', 'x', 'x', 'x']
hand_2 = ['2', '3', '3', '4', '4', '5', '6']
hand_3 = ['x', 'x', 'x', 'x', 'x', 'x']

pile = []

assert (len(hand_1) + len(hand_2) + len(hand_3)) % 4 == 0

turn = [hand_1, hand_2, hand_3]
goes = 0

def update_pile(turn, goes, pile):
    ''' A hand passes some (1-4) cards to the pile.
        Returns updated pile. '''
    passing = []
    cards_num = randint(1, min(4, len(turn[goes])))
    for num in range(cards_num):
        card = randint(0, len(turn[goes]) - 1)
        passing.append(turn[goes][card])
        del turn[goes][card]
    pile += passing
    return pile

def is_empty(turn, goes):
    ''' Checks if the hand played has become empty.
        Returns True / False. '''
    if len(turn[goes]) == 0:
        return True
    else:
        return False

def update_turn(goes):
    ''' Updates the hand that goes next. '''
    if goes != len(turn)-1:
        goes += 1
    else:
        goes = 0
    return goes

def printing(hand_1, hand_2, hand_3, pile):
    ''' Prints the results of the turn. '''
    print('1', hand_1)
    print('2', hand_2)
    print('3', hand_3)
    print('pile', pile, '\n')

def winner(goes):
    ''' Announes a winner hand. '''
    print("The winner is hand " + str(goes+1) + "!")
    

def game_loop(hand_1, hand_2, hand_3, turn, goes, pile):
    
    # The game ends as soon as one hand is empty.
    empty = False
    while not empty:
        pile = update_pile(turn, goes, pile)
        printing(hand_1, hand_2, hand_3, pile)
        empty = is_empty(turn, goes)
        if not empty:
            goes = update_turn(goes)
    winner(goes)

game_loop(hand_1, hand_2, hand_3, turn, goes, pile)
