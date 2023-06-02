#!/usr/bin/env python3

import os
import random
import time
import pickle

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

# Initialize the attributes of the DigiPet
class DigiPet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.age = 0
        self.feelings = 'Happy'
        self.status = 'Healthy'
        self.position = [5, 5]

    def info(self):
        print(f'\n\nName: {self.name}\nHunger: {self.hunger}\nAge: {self.age}\nFeelings: {self.feelings}\nStatus: {self.status}\n\n')

    def move(self):
        self.position = [random.randint(0, 30), random.randint(0, 10)]
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

# Main program
if __name__ == "__main__":
    # Create the directory for the data file if it does not exist
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    try:
        # Load existing pet
        with open(DATA_FILE, 'rb') as file:
            pet = pickle.load(file)
    except (FileNotFoundError, EOFError):
        # If there's no existing pet, ask for a name to create a new one
        pet_name = input("What do you want to name your DigiPet? ")
        pet = DigiPet(pet_name)

    while True:
        os.system('clear')  # Clear the terminal

        # Print spaces to simulate movement
        print('\n' * pet.position[1], end='')  # Move Down
        print(' ' * pet.position[0], end='')  # Move Right
        print(dog)  # Display the ASCII dog

        print("\n\n1. Info | 2. Feed | 3. Play | 4. Move | 5. Start New Game | 6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            pet.info()
            time.sleep(2)  # Pause to allow reading
        elif choice == "2":
            pet.feed()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            pet.move()
        elif choice == "5":
            # Start a new game
            pet_name = input("What do you want to name your new DigiPet? ")
            pet = DigiPet(pet_name)
        elif choice == "6":
            break
        else:
            print("Invalid option. Please choose a valid option.")

        # Save the pet's data
        with open(DATA_FILE, 'wb') as file:
            pickle.dump(pet, file)

        time.sleep(1)  # Pause between actions
