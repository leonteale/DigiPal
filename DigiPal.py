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

exclamation_point = """
 !
 !
 !
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
        self.feelings = 'Full'
        self.status = 'Unhealthy'
        self.position = [terminal_size[0]//2, terminal_size[1]//2]
        self.terminal_size = terminal_size
        self.boundary = [terminal_size[0]//2, terminal_size[1]//2]
        self.last_activity = datetime.datetime.now()
        self.death_time = None
        self.feed_count = 0
        self.last_feed_time = None
        self.happiness = random.randint(50, 75)
        self.play_count = 0
        self.last_play_time = None
        self.tiredness = 0
        self.sleep_time = None

    def info(self):
        print(f'Hunger: {self.hunger} | Happiness: {self.happiness} | Age: {self.age} | Feelings: {self.feelings} | Status: {self.status} | Tiredness: {self.tiredness}')

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

        if self.tiredness >= 90:
            self.status = 'Tired'
            self.sleep()
        elif self.hunger <= 40:
            self.status = 'Unhealthy'
        else:
            self.status = 'Healthy'

        if self.status == 'Sleeping' and datetime.datetime.now() >= self.sleep_time:
            self.status = 'Healthy'
            self.sleep_time = None
            self.happiness = random.randint(50, 75)

    def feed(self):
        if self.status == 'Dead' or self.status == 'Sleeping':
            return
        now = datetime.datetime.now()
        if self.last_feed_time is not None and (now - self.last_feed_time).total_seconds() <= 30:
            self.feed_count += 1
        else:
            self.feed_count = 1
        self.last_feed_time = now

        if self.feed_count > 3 and (now - self.last_feed_time).total_seconds() <= 30:
            self.feelings = 'Overfed'
            self.hunger = min(100, self.hunger + random.randint(1, 5)) # Overfeeding only slightly increases hunger
            self.status = 'Unhealthy' if random.random() < 0.1 else self.status # 10% chance of becoming unhealthy due to overfeeding
            self.tiredness = min(100, self.tiredness + 35)
        else:
            self.hunger = min(100, self.hunger + random.randint(5, 20))

    def play(self):
        if self.status == 'Dead' or self.status == 'Sleeping':
            return
        now = datetime.datetime.now()
        if self.last_play_time is not None and (now - self.last_play_time).total_seconds() <= 30:
            self.play_count += 1
        else:
            self.play_count = 1
        self.last_play_time = now

        if self.play_count > 3 and (now - self.last_play_time).total_seconds() <= 30:
            self.feelings = 'Overjoyed'
            self.happiness = min(100, self.happiness + random.randint(1, 5)) # Overplaying only slightly increases happiness
            self.status = 'Unhealthy' if random.random() < 0.1 else self.status # 10% chance of becoming unhealthy due to overplaying
            self.tiredness = min(100, self.tiredness + 35)
        else:
            self.happiness = min(100, self.happiness + random.randint(5, 35))
            self.tiredness = min(100, self.tiredness + random.randint(1, 10))

    def sleep(self):
        if self.status != 'Tired':
            return
        self.status = 'Sleeping'
        self.sleep_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
        self.tiredness = 0

    def get_sleep_time_left(self):
        if self.status != 'Sleeping':
            return 0
        return max(0, (self.sleep_time - datetime.datetime.now()).total_seconds())

def get_terminal_size():
    rows, cols = os.popen('stty size', 'r').read().split()
    return int(rows), int(cols)

def display_quick_stats(pet):
    print(f'Hunger: {pet.hunger} | Happiness: {pet.happiness} | Age: {pet.age} | Feelings: {pet.feelings} | Status: {pet.status} | Tiredness: {pet.tiredness}')

def print_menu(sleep_time_left=0):
    if sleep_time_left > 0:
        minutes = int(sleep_time_left // 60)
        seconds = int(sleep_time_left % 60)
        print(f"Pet is sleeping. Zzz... Time left: {minutes} minutes {seconds} seconds")
    else:
        print("1. Display full stats | 2. Feed pet | 3. Play with pet | 4. Create a new pet | 5. Exit")

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
        if not hasattr(pet, 'last_feed_time'):
            pet.last_feed_time = datetime.datetime.now()
        if not hasattr(pet, 'feed_count'):
            pet.feed_count = 0
        if datetime.datetime.now() - pet.last_activity > datetime.timedelta(hours=1):
            pet.hunger = max(0, pet.hunger - random.randint(20, 60))
    else:
        pet_name = input('Please name your pet: ')
        pet = DigiPal(pet_name, terminal_size)

    while pet.status != 'Dead':
        os.system('clear')  # Clear the terminal screen
        print(dog)
        display_quick_stats(pet)
        print_menu(pet.get_sleep_time_left())

        if pet.status == 'Sleeping':
            time.sleep(0.2)
            continue

        selection = get_key()
        if selection == '1':
            pet.info()
        elif selection == '2':
            pet.feed()
        elif selection == '3':
            pet.play()
        elif selection == '4':
            pet_name = input('Please name your new pet: ')
            pet = DigiPal(pet_name, terminal_size)
        elif selection == '5':
            pet.last_activity = datetime.datetime.now()
            with open(DATA_FILE, 'wb') as file:
                pickle.dump(pet, file)
            print('Game saved and exited.')
            break
        else:
            print("Invalid selection, please try again.")

        if pet.status == 'Dead':
            print(grave)
            break

        pet.move()
        time.sleep(0.2)
        if pet.tiredness >= 100:
            pet.sleep()
