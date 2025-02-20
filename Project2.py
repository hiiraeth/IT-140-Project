import time as t
import keyboard as kb

# defines a class for each room
class Room:
    def __init__(self, name, directions, items=None):
        self.name = name
        self.directions = directions or {}
        self.items = items or None

    # allows items to be removed from room, used when items get picked up
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

# displays how to play the game
def instructions(list):
    print('| Welcome to the game! Before you begin, here are the instructions:')
    t.sleep(1.5)

    print('| The goal of the game is to move around the executive floor and collect six items in different rooms, '
            'and to not get caught by the security robot, who is hiding in one of the rooms')
    t.sleep(1.5)

    print('| You lose the game if the security robot catches you.')
    t.sleep(1.5)

    print('| You win the game by collecting all six items, which are:')
    
    for item in list:
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

# displays users inventory
def show_items(items):
    if not items:
        print('\n| Your inventory is empty.')
        return # exits function if inventory is empty

    print('\n| Your current items are:')
    for item in items: # prints out items user currently has in inventory
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

    # checks to see if the current room has an item
    if current_room.items is None or not current_room.items:
        print(f'\n| There are no items in {current_room.name}.')
    else:
        print('\n| There is an item in this room!\n|--', *current_room.items)

# allows user to make a decision; whether to use the move action, or item action
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

# lets user move between rooms
def move_action(current_room):
    while True:
        print('| Please make your selection by typing the direction:', end=' ')
        direction = str(input().strip().capitalize())

        if direction == 'Exit':
            quit()
            print('\nThanks for playing! :)')

        # validates the direction variable
        if direction in current_room.directions:
            new_room = current_room.directions[direction]
            if new_room not in rooms: # in case some type of critical error occurs
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

    return rooms[new_room] # returns the room that user chose to move to

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

    print('\n-------------------------------------------------------------------')
    print(f'{'You lost the game':^67}')
    print('-------------------------------------------------------------------\n')
    t.sleep(1)

# displays game winning sequence
def game_win():
    print('\n-------------------------------------------------------------------')
    print(f'{'Congratulations!!':^67}')
    print('-------------------------------------------------------------------\n')     

    t.sleep(2)
    print('You won the game!')
    t.sleep(1)

    print('I hope you enjoyed playing it.')
    t.sleep(2)

    print('Goodbye for now!')
    t.sleep(2)


# asks user if they want to play again
def play_again():
    answer = input('Play again? Y/N: ').strip().lower()

    if answer == 'y': # restarts from the intro
        intro_to_game()
    else:
        print('\nThanks for playing! :)')
        quit()

    return rooms['Lobby'] # resets users room to starting room, the lobby
                          # the inventory gets reset in the main game loop

# allows user to pick up or ignore an item
def item_action(room, item):
    # loops until user enters a valid command
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
            
            room.remove_item(item) # removes the item from the room, so it cannot be picked up again
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

# main game function
def main():
    # initializing variables
    item_list = ['BLUEPRINTS', 'MANIFESTO', 'MITM', 'FINANCE REPORTS', 'ROLODEX', 'KEY CARD']
    current_room = rooms['Lobby']
    inventory = []

    # output game info to user
    intro_to_game()
    instructions(item_list)

    # main loop, will execute infinitely until user exits, loses, or wins
    while True:
        # boolean to check with each loop to see if user has all required items
        isAllItems = all(item in inventory for item in item_list)

        if current_room == rooms['CEO Suite']: # checks if user is in room w/ villain
            game_over()
            current_room = play_again()
            inventory = []
            continue
        if isAllItems == True:
            game_win()
            play_again()
            inventory = []
            continue
        
        # outputs current room info and users inventory to user
        room_information(current_room)
        t.sleep(0.8)

        show_items(inventory)
        t.sleep(0.8)

        # validates choice variable
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