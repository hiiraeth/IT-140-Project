#TODO: finish inventory system
#TODO: implement item collection feature: actually collecting items, 
#      removing item from room after collection, updating inventory
#TODO: update intro to include the list of items (or output them somewhere)
#TODO: add win-check to main game loop (need the 6 required items)
#TODO: add option for user to exit game
#TODO: clean up comments, update and add them as needed

import time as t
import keyboard as kb

class Room:
    def __init__(self, name, directions, items=None):
        self.name = name
        self.directions = directions or {}
        self.items = items or None

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

# dictionary of all the rooms and their instances
rooms = {
    'CEO Suite': Room('CEO Suite', {'South': 'Technology Lab','East': 'Library'}, []),
    'Lobby': Room('Lobby', {'North': 'Conference Room', 'East': 'Break Room', 'West': 'Operations'}, []),
    'Utility Closet': Room('Utility Closet', {'North': 'Technology Lab'}, []),
    'Library': Room('Library', {'South': 'Conference Room', 'East': 'CFO Suite', 'West': 'CEO Suite'}, 
                    ['MANIFESTO']),
    'CFO Suite': Room('CFO Suite', {'South': 'Break Room', 'West': 'Library'},
                      ['FINANCE REPORTS']),
    'Break Room': Room('Break Room', {'North': 'CFO Suite', 'West': 'Lobby'},
                       ['DR. PEPPER']),
    'Conference Room': Room('Conference Room', {'North': 'Library', 'South': 'Lobby', 'West': 'Technology Lab'},
                            ['ROLODEX']),
    'Operations': Room('Operations', {'South': 'Security', 'East': 'Lobby', 'West': 'Technology Lab'},
                       ['KEY CARD']),
    'Security': Room('Security', {'North': 'Operations'},
                     ['BLUEPRINTS']),
    'Technology Lab': Room('Technology Lab', {'North': 'CEO Suite', 'Northeast': 'Conference Room', 
                            'Southeast': 'Operations', 'South': 'Utility Closet'},
                            ['MITM'])
}

# displays intro message to user. can be skipped by pressing space bar.
def intro_to_game(): 
    lines = [ # list of intro dialogue
        'You find yourself in the year 2945.',
        'The Earth became uninhabitable centuries ago, and you’re working for a faction on the new, neon-lit futuristic planet you live on.',
        'The head of operations gave you a mission—to infiltrate another faction’s headquarters and gather information on their operations without getting caught. You must work your way around their executive floor.',
        'You try not to worry as you have completed similar missions in the past, but this time, you do not have a clue as to what the layout of the floor is like or where anything is.',
        'There is a security robot hiding in one of the rooms. You must avoid it at all costs.',
        'If you get caught, you will be exiled from the faction and left to fend for yourself in the barren wastelands.',
        'To complete the mission, the head of operations is requiring you to collect 6 specific items. Will you be able to succeed?\n',
        '-------------------------------------------------------------------'
    ]

    print('\nTo skip intro, press the space bar at anytime.\n')
    t.sleep(0.5)

    # prints intro message, and detects space keystroke to skip intro
    for line in lines:
        print(line)

        time = 0 
        while time < 3:
            if kb.is_pressed('space'):
                print('\nStarting game...\n')
                t.sleep(1.5)
                return
            t.sleep(0.1)  # allows program to skip intro at any moment 
            time += 0.1   # and not just in between .sleep() statements

    t.sleep(2)

def instructions():
    item_list = ('BLUEPRINTS', 'MANIFESTO', 'MITM', 'FINANCE REPORTS', 'ROLODEX', 'KEY CARD')

    print('| Welcome to the game! Before you begin, here are the instructions:')
    t.sleep(1.5)

    print('| The goal of the game is to move around the executive floor and collect six items in different rooms, '
            'and to not get caught by the security robot, who is hiding in one of the rooms')
    t.sleep(1.5)

    print('| You lose the game if the security robot catches you.')
    t.sleep(1.5)

    print('| You win the game by collecting all six items, which are:')
    
    for item in item_list:
        print(f'|-- {item}')
    t.sleep(4)

    print('| There is an optional item in one of the rooms.\n')
    t.sleep(2)

    print('| To exit the game at any point, type \'EXIT\' into any input prompt.')
    t.sleep(1.5)

    start_end = input('| Ready to begin? (Any/EXIT): ').strip().lower()
    if start_end == 'exit':
        quit()
    else:
        print('\nLet\'s begin!')
        t.sleep(1)
        print('\n-------------------------------------------------------------------')
        print(f'{'Heading to Lobby...':^67}')
        print('-------------------------------------------------------------------\n')
        t.sleep(2)


def show_items(items):
    print('\n| Your current items are:')
    if not items:
        print('|-- Your inventory is empty.')

    for item in items:
        print(f'|-- {item}')

# displays info about room user is currently in to user, such as connections to other rooms
def room_information(current_room):
    i = 1 # counter for loop, numbers the list of rooms                 

    if current_room.name != 'Operations':
        print(f'| You are currently in the {current_room.name}. The adjacent rooms are:')
    else: 
        print(f'| You are currently in {current_room.name}. The adjacent rooms are:')

    for direction, room in current_room.directions.items(): # iterates thru all the valid 
        print(f'|-- {i}) {room:<15} | {direction:>5}')      # directions and displays to user
        i += 1
    
    t.sleep(0.8)
    if current_room.items is None or not current_room.items:
        print(f'\n| There are no items in {current_room.name}.')
    else:
        print('\n| There is an item in this room!\n|--', *current_room.items)

def player_choice():
    while True:
        choice = str(input('\n| What would you like to do? Enter \'M\' to move rooms or '
                           '\'I\' to pick up items: ').strip().lower())

        if (choice == 'm') or (choice == 'i'):
            return choice
        elif choice == 'exit':
            quit()
            print('\nThanks for playing! :)')
        else:
            print('Please enter a valid command.')
            continue

def move_action(current_room):
    while True:
        print('| Please make your selection by typing the direction:', end=' ')
        direction = str(input().strip().capitalize())

        if direction == 'exit':
            quit()
            print('\nThanks for playing! :)')

        if direction in current_room.directions:
            new_room = current_room.directions[direction]
            if new_room not in rooms:
                print('Uh oh, that room does not exist.')
                continue
            break
        else:
            print(f'{direction} is not a valid direction. Please try again.\n')
            t.sleep(1)
            continue

    print('\n-------------------------------------------------------------------')
    print(f'{f'Heading to {new_room}...':^67}')
    print('-------------------------------------------------------------------\n')
    t.sleep(2)

    return rooms[new_room]

# displays game over sequence
def game_over():
    t.sleep(1)
    print('Uh oh...')
    t.sleep(3)

    print('Oh no! You were caught by the security robot.')
    t.sleep(2)

    print('You had a nice run.')
    t.sleep(2)

    print('I wish the best for you.')
    t.sleep(2)

    print('Goodbye.\n')
    t.sleep(3)

# asks user if they want to play again
def play_again():
    answer = input('Play again? Y/N: ').strip().lower()

    if answer == 'y': # restarts from the intro
        intro_to_game()
        #FIXME: reset inventory and items once implemented
    else:
        print('\nThanks for playing! :)')
        quit()

    return rooms['Lobby']

#FIXME: implement 
def item_action(room, item):
    while True:
        if not room.items:
            print('There are no items to pick up!')
            break
        elif room.items[0] in item:
            print('You already have this item!')
            break

        choice = input('| Would you like to pick up the item? (Y/N): ').strip().lower()

        if choice == 'y':
            item = room.items[0]

            print('\n-------------------------------------------------------------------')
            print(f'{f'{room.items[0]} has been added to your inventory.':^67}')
            print('-------------------------------------------------------------------\n')
            
            room.remove_item(item)
            return item
        elif choice == 'n':
            print(f'You did not pick up {room.items[0]}.')
            break
        elif choice == 'exit':
            quit()
            print('\nThanks for playing! :)')
        else: 
            print('Please enter a valid command.')
            continue

# main game function:
# -- will display room information
# -- moves user based on user input
# -- decides if game is won or lost
# -- checks for villain
def main():
    # initializing variables
    current_room = rooms['Lobby']
    inventory = []

   # intro_to_game() # outputs intro to user
    instructions()

    # main loop, will execute infinitely until user exits, loses, or wins
    while True:
        if current_room == rooms['CEO Suite']: # checks if user is in room w/ villain
            game_over()
            current_room = play_again()
            continue
        elif len(inventory) == 7:
            print('You win!')
            quit()
        
        #FIXME: add win check system

        room_information(current_room)
        t.sleep(0.8)

        show_items(inventory)
        t.sleep(0.8)

        while True:
            choice = player_choice()

            if choice == 'm':
                current_room = move_action(current_room)
                break
            elif choice == 'i':
                item = item_action(current_room, inventory)
                if item is not None:
                    inventory.append(item)
                    t.sleep(1.5)
                    break
                t.sleep(1.5)

if __name__ == '__main__':
    main()