import time as t
import keyboard as kb

# displays intro message to user. can be skipped by pressing space bar.
def intro_to_game(): 
    lines = [ # list of intro dialogue
        'You find yourself in the year 2945.',
        'The Earth became uninhabitable centuries ago, and you’re working for a faction on the new, neon-lit futuristic planet you live on.',
        'The head of operations gave you a mission—to infiltrate another faction’s headquarters and gather information on their operations without getting caught. You must work your way around their executive floor.',
        'You try not to worry as you have completed similar missions in the past, but this time, you do not have a clue as to what the layout of the floor is like or where anything is.',
        'There is a security robot hiding in one of the rooms. You must avoid it at all costs.',
        'If you get caught, you will be exiled from the faction and left to fend for yourself in the barren wastelands.',
        'To complete the mission, the head of operations is requiring you to collect 6 specific items. Will you be able to succeed?\n'
        '---------------------------------------\n'
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


    print('Welcome to the game! You are starting off in the lobby.\n')
    t.sleep(2)

# displays info about room user is currently in to user, asks what direction they want to move
def room_information(current_room):
    i = 1 # counter for loop                 # holds all adjacent rooms to current room
    directions = rooms[current_room].items() # and valid movement directions 

    if current_room != 'Operations':
        print(f'| You are currently in the {current_room}. The adjacent rooms are:')
    else: 
        print(f'| You are currently in {current_room}. The adjacent rooms are:')

    for direction, room in directions: # iterates thru all valid directions to display to user
        print(f'|-- {i}) {room:<15} | {direction:>5}')
        i += 1
    
    print('| Please make your selection by typing the direction. Type \'Exit\' to quit:', end=' ')
    direction = str(input().strip().capitalize())

    return direction

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

# makes sure room is valid, and returns that room.
# room will update for player once main loop repeats
def update_room(current_room, new_room):
    if new_room not in rooms:
        print('Uh oh, that room does not exist.')
    
    current_room = new_room
    print(f'\nHeading to {new_room}...\n')
    t.sleep(2)

    return current_room

# asks user if they want to play again
def play_again():
    answer = input('Play again? Y/N: ').strip().lower()

    if answer == 'y': # restarts from the intro
        current_room = 'Lobby'
        direction = None
        intro_to_game()
    else:
        print('\nThanks for playing this abridged version of the game! :)')
        quit()

# dictionary of all the rooms and their valid directions
rooms = {
    'CEO Suite': 
        {'South': 'Technology Lab',
         'East': 'Library'},
    'Library': 
        {'South': 'Conference Room',
         'East': 'CFO Suite',
         'West': 'CEO Suite'},
    'CFO Suite': 
        {'South': 'Break Room',
         'West': 'Library'},
    'Break Room':
        {'North': 'CFO Suite',
         'West': 'Lobby'},
    'Lobby': 
        {'North': 'Conference Room', 
         'East': 'Break Room', 
         'West': 'Operations'},
    'Conference Room': 
        {'North': 'Library',
         'South': 'Lobby',
         'West': 'Technology Lab'},
    'Technology Lab': 
        {'North': 'CEO Suite',
         'Northeast': 'Conference Room',
         'Southeast': 'Operations', 
         'South': 'Utility Closet'},
    'Utility Closet':
        {'North': 'Technology Lab'},
    'Operations':
        {'South': 'Security',
         'East': 'Lobby',
         'West': 'Technology Lab'},
    'Security':
        {'North': 'Operations'}
}

# main game function:
# - will display room information
# - moves user based on user input
# - decides if game is won or lost
# - checks for villain
def main():
    # initalizing variables
    current_room = 'Lobby'
    direction = None

    intro_to_game() # outputs intro to user

    # main loop, will execute infinitely until user exits, loses, or wins (to be added)
    while True:
        if current_room == 'CEO Suite': # checks if user is in room w/ villain
            game_over()
            play_again()
            continue

        direction = room_information(current_room)
        
        # branching to check user input, proceeds accordingly
        if direction in rooms[current_room]:
            next_room = rooms[current_room][direction]
        elif direction == 'Exit':
            play_again()
            continue
        else:
            print(f'\n{direction} is not a valid direction. Please try again.\n')
            t.sleep(1)
            continue

        current_room = update_room(current_room, next_room)

if __name__ == '__main__':
    main()