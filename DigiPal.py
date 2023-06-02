#!/usr/bin/env python3

import os
import random
import time
import pickle
import signal
import termios
import sys
import tty
import datetime

# ASCII Art for the DigiPal
dog = """
 / \__
(    @\__ 
 /         O
/   (_____/
/_____/ U
"""

grave = """
_______
| RIP |
|     |
|     |
|     |
|_____|
"""

# Directory to store the DigiPal's data
DATA_DIRECTORY = os.path.expanduser('~/.DigiPal')
DATA_FILE = os.path.join(DATA_DIRECTORY, 'data.pickle')

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

# Initialize the attributes of the DigiPal
class DigiPal:
    def __init__(self, name, terminal_size):
        self.name = name
        self.hunger = 50
        self.age = 0
        self.date_of_birth = datetime.date.today()
        self.feelings = 'Happy'
        self.status = 'Healthy'
        self.position = [terminal_size[0]//2, terminal_size[1]//2]
        self.terminal_size = terminal_size
        self.boundary = [terminal_size[0]//2, terminal_size[1]//2]
        self.last_activity = datetime.datetime.now()
        self.death_time = None

    def info(self):
        print(f'\n\nName: {self.name}\nHunger: {self.hunger}\nDate of Birth: {self.date_of_birth}\nAge: {(datetime.date.today() - self.date_of_birth).days}\nFeelings: {self.feelings}\nStatus: {self.status}\n\n')

    def move(self):
        if self.hunger <= 0 and (self.death_time is None or (datetime.datetime.now() - self.death_time).total_seconds() >= 5 * 60):
            self.status = 'Dead'
            return
        elif self.hunger <= 0 and self.death_time is None:
            self.death_time = datetime.datetime.now()

        new_position = [random.randint(0, self.boundary[0]), random.randint(0, self.boundary[1])]
        if 0 <= new_position[0] < self.boundary[0] and 0 <= new_position[1] < self.boundary[1]:
            self.position = new_position

        if (datetime.datetime.now() - self.last_activity).total_seconds() >= random.randint(1, 5) * 60:
            self.hunger = max(0, self.hunger - random.randint(1, 5))
            self.last_activity = datetime.datetime.now()

        if self.hunger <= 20:
            self.feelings = 'Hungry'
        elif self.hunger <= 40:
            self.feelings = 'Okay'
        else:
            self.feelings = 'Full'

    def feed(self):
        if self.status == 'Dead':
            return
        self.hunger = min(100, self.hunger + 20)

    def play(self):
        if self.status == 'Dead':
            return
        self.hunger = max(0, self.hunger - 10)

def get_terminal_size():
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(rows), int(cols)

def draw_border(pet):
    print('\033[47m' + ' ' * (pet.boundary[0] + 2) + '\033[0m')  # Top border
    for _ in range(pet.boundary[1]):
        print('\033[47m' + ' \033[0m' + ' ' * pet.boundary[0] + '\033[47m' + ' \033[0m')  # Side borders
    print('\033[47m' + ' ' * (pet.boundary[0] + 2) + '\033[0m')  # Bottom border

def display_quick_stats(pet):
    print(f'\n\nHunger: {pet.hunger} | Age: {pet.age} | Feelings: {pet.feelings}\n\n')

def create_data_directory():
    """
    Create the data directory if it doesn't exist.
    """
    os.makedirs(DATA_DIRECTORY, exist_ok=True)

def signal_handler(sig, frame):
    # Save the pet's data when the game is exited with ctrl+c
    pet.last_activity = datetime.datetime.now()
    with open(DATA_FILE, 'wb') as file:
        pickle.dump(pet, file)
    print('Game saved and exited.')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    create_data_directory()

    terminal_size = get_terminal_size()

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as file:
            pet = pickle.load(file)
        if not hasattr(pet, 'boundary'):
            pet.position = [terminal_size[0]//2, terminal_size[1]//2]
            pet.boundary = [terminal_size[0]//2, terminal_size[1]//2]
        pet.last_activity = datetime.datetime.now()
        if datetime.datetime.now() - pet.last_activity > datetime.timedelta(hours=1):
            pet.hunger = max(0, pet.hunger - random.randint(20, 60))
    else:
        pet_name = input("What do you want to name your DigiPal? ")
        pet = DigiPal(pet_name, terminal_size)

    while True:
        os.system('clear')

        draw_border(pet)

        print('\n' * pet.position[1], end='')
        print(' ' * pet.position[0], end='')
        if pet.status == 'Dead':
            print(grave)
        else:
            print(dog)

        display_quick_stats(pet)

        print('\n\n1. info  | 2. feed  | 3. play  | 4. exit  | 5. new pet\n\n')

        pet.move()

        choice = get_key()

        if choice == "1":
            pet.info()
            time.sleep(2)
        elif choice == "2":
            pet.feed()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            break
        elif choice == "5":
            pet_name = input("What do you want to name your new DigiPal? ")
            pet = DigiPal(pet_name, terminal_size)
        else:
            print("Invalid option. Please choose a valid option.")

        with open(DATA_FILE, 'wb') as file:
            pickle.dump(pet, file)

    with open(DATA_FILE, 'wb') as file:
        pickle.dump(pet, file)
    print('Game saved and exited.')
