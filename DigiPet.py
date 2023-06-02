#!/usr/bin/env python3

import os
import random
import time
import pickle
import signal
import termios
import sys
import tty

# ASCII Art for the DigiPet
dog = """
 / \__
(    @\__ 
 /         O
/   (_____/
/_____/ U
"""

# File to store the DigiPet's data
DATA_FILE = os.path.expanduser('~/.DigiPet/data.pickle')

def get_key():
    """
    Wait for a key press and return a single character string.
    """
    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
    return ch

# Initialize the attributes of the DigiPet
class DigiPet:
    def __init__(self, name, terminal_size):
        self.name = name
        self.hunger = 50
        self.age = 0
        self.feelings = 'Happy'
        self.status = 'Healthy'
        self.position = [terminal_size[1]//2, terminal_size[0]//2]
        self.terminal_size = terminal_size
        self.boundary = [terminal_size[1]//2, terminal_size[0]//4]

    def info(self):
        print(f'\n\nName: {self.name}\nHunger: {self.hunger}\nAge: {self.age}\nFeelings: {self.feelings}\nStatus: {self.status}\n\n')

    def move(self):
        new_position = [random.randint(0, self.boundary[0]), random.randint(0, self.boundary[1])]
        if 0 <= new_position[0] < self.boundary[0] and 0 <= new_position[1] < self.boundary[1]:
            self.position = new_position
        self.hunger -= 5

    def feed(self):
        if self.hunger < 100:
            self.hunger += 10
        else:
            print(f'{self.name} is already full.')

    def play(self):
        if self.feelings != 'Excited':
            self.feelings = 'Excited'
        else:
            print(f'{self.name} is already excited')

def get_terminal_size():
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(rows), int(cols)

def draw_border(pet):
    print('\033[47m' + ' ' * (pet.boundary[0] + 2) + '\033[0m')  # Top border
    for _ in range(pet.boundary[1]):
        print('\033[47m \033[0m' + ' ' * pet.boundary[0] + '\033[47m \033[0m')  # Side borders
    print('\033[47m' + ' ' * (pet.boundary[0] + 2) + '\033[0m')  # Bottom border

def display_quick_stats(pet):
    print(f'\n\nHunger: {pet.hunger}\nAge: {pet.age}\nFeelings: {pet.feelings}\n\n')

def signal_handler(sig, frame):
    # Save the pet's data when the game is exited with ctrl+c
    with open(DATA_FILE, 'wb') as file:
        pickle.dump(pet, file)
    print('Game saved and exited.')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    terminal_size = get_terminal_size()

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as file:
            pet = pickle.load(file)
        if not hasattr(pet, 'boundary'):
            # The pet object was saved by an older version of the script and needs to be updated
            pet.position = [terminal_size[1]//2, terminal_size[0]//2]
            pet.boundary = [terminal_size[1]//2, terminal_size[0]//4]
    else:
        pet_name = input("What do you want to name your DigiPet? ")
        pet = DigiPet(pet_name, terminal_size)

    while True:
        os.system('clear')  # Clear the terminal

        draw_border(pet)

        # Print spaces to simulate movement
        print('\n' * pet.position[1], end='')  # Move Down
        print(' ' * pet.position[0], end='')  # Move Right
        print(dog)  # Display the ASCII dog

        display_quick_stats(pet)

        print('\n\n1. info  | 2. feed  | 3. play  | 4. exit  | 5. new pet\n\n')
        time.sleep(2)
        pet.move()

        choice = get_key()

        if choice == "1":
            pet.info()
            time.sleep(2)  # Pause to allow reading
        elif choice == "2":
            pet.feed()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            break
        elif choice == "5":
            # Start a new game
            pet_name = input("What do you want to name your new DigiPet? ")
            pet = DigiPet(pet_name, terminal_size)
        else:
            print("Invalid option. Please choose a valid option.")

        # Save the pet's data
        with open(DATA_FILE, 'wb') as file:
            pickle.dump(pet, file)

    # Save the pet's data when the game is exited normally
    with open(DATA_FILE, 'wb') as file:
        pickle.dump(pet, file)
    print('Game saved and exited.')
