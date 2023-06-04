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
import math

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

DATA_DIRECTORY = os.path.expanduser('~/.DigiPal')
DATA_FILE = os.path.join(DATA_DIRECTORY, 'data.pickle')

def get_key():
    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
    return ch

class DigiPal:
    def __init__(self, name, terminal_size):
        self.name = name
        self.hunger = 50
        self.age = 0
        self.date_of_birth = datetime.date.today()
        self.feelings = 'Full'
        self.status = 'Healthy'
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
            self.hunger = max(0, self.hunger - random.randint(1, 10))
            self.last_activity = datetime.datetime.now()

        if self.hunger <= 20:
            self.feelings = 'Hungry'
        elif self.hunger <= 40:
            self.feelings = 'Okay'
        else:
            self.feelings = 'Full'

        if self.tiredness >= 100 and self.status != 'Sleeping':
            self.sleep()
        elif self.hunger <= 40:
            self.status = 'Unhealthy'
        elif self.hunger >= 100:
            self.status = 'Over-fed'
            self.happiness = math.floor(self.happiness / 2)

    def feed(self):
        if self.status != 'Dead' and self.status != 'Sleeping':
            self.hunger = min(100, self.hunger + random.randint(5, 15))
            self.tiredness = min(100, self.tiredness + random.randint(5, 15))
            if self.hunger >= 100:
                self.status = 'Over-fed'
                self.happiness = math.floor(self.happiness / 2)
        else:
            print('Cannot feed DigiPal at the moment.')

    def play(self):
        if self.status != 'Dead' and self.status != 'Sleeping':
            self.happiness = min(100, self.happiness + random.randint(1, 10))
            self.tiredness = min(100, self.tiredness + random.randint(5, 25))
        else:
            print('Cannot play with DigiPal at the moment.')

    def get_sleep_time_left(self):
        if self.status == 'Sleeping':
            return max(0, (self.sleep_time - datetime.datetime.now()).total_seconds())
        else:
            return 0

    def sleep(self):
        if self.status != 'Tired':
            return
        self.status = 'Sleeping'
        self.sleep_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
        time.sleep(30)  # sleep for 30 seconds
        self.tiredness = 20
        self.status = 'Refreshed'

def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)

def display_quick_stats(pet):
    print(f'Hunger: {pet.hunger} | Happiness: {pet.happiness} | Age: {pet.age} | Feelings: {pet.feelings} | Status: {pet.status} | Tiredness: {pet.tiredness}')

def print_menu(sleep_time_left=0):
    if sleep_time_left > 0:
        print(f"DigiPal is sleeping. Zzz... Time left: {int(sleep_time_left)} seconds")
    else:
        print("1. Feed DigiPal | 2. Play with DigiPal | 3. Check DigiPal stats | q. Quit")

def main():
    os.system('clear')
    terminal_size = get_terminal_size()

    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)

    if not os.path.exists(DATA_FILE):
        name = input('What is the name of your DigiPal: ')
        pet = DigiPal(name, terminal_size)
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(pet, f)
    else:
        with open(DATA_FILE, 'rb') as f:
            pet = pickle.load(f)

    while True:
        os.system('clear')
        print(dog if pet.status != 'Dead' else grave)
        print(f'DigiPal name: {pet.name}')
        display_quick_stats(pet)

        sleep_time_left = pet.get_sleep_time_left()
        print_menu(sleep_time_left)

        if pet.status == 'Dead':
            print('Your DigiPal is dead. Please start a new game.')
            break

        if sleep_time_left <= 0:
            user_choice = get_key().lower()
            if user_choice == '1':
                pet.feed()
            elif user_choice == '2':
                pet.play()
            elif user_choice == '3':
                pet.info()
                time.sleep(3)
            elif user_choice == 'q':
                break

        pet.move()

        with open(DATA_FILE, 'wb') as f:
            pickle.dump(pet, f)

        time.sleep(1)

if __name__ == "__main__":
    main()
