#!/usr/bin/env python

import os
import random
import time
from blessed import Terminal
from pet_initialization import initialize_pet
from pet_display import display_pet, clear_screen, pet_ascii
from pet_menu import display_menu

# Initialize the terminal
term = Terminal()

# Define the dimensions of the pet's square box and menu
box_width = 40
box_height = 10
menu_height = 5

# Initial position of the pet
pet_x = box_width // 2
pet_y = box_height // 2

# Function to move the pet
def move_pet():
    global pet_x, pet_y

    # Generate random movements within a larger range
    dx = random.randint(-2, 2)
    dy = random.randint(-2, 2)

    # Update the pet's position
    pet_x += dx
    pet_y += dy

    # Keep the pet within the boundaries of the box
    pet_x = max(2, min(pet_x, box_width - len(pet_ascii.split('\n')[0]) - 2))
    pet_y = max(2, min(pet_y, box_height - pet_ascii.count('\n') - 2))

# Function to display the pet and menu
def display_pet_and_menu():
    with term.location(0, 0):
        # Draw the box
        print(term.white('─' * box_width))
        for _ in range(box_height - 2):
            print(term.white('│' + ' ' * (box_width - 2) + '│'))
        print(term.white('─' * box_width))

        # Display the pet
        display_pet(pet_x, pet_y)

        # Display the menu
        display_menu()

# Main function
def main():
    # Check if the data file exists
    data_file = os.path.expanduser("~/.Digipet/data.txt")
    if not os.path.exists(data_file):
        initialize_pet()

    with term.fullscreen(), term.hidden_cursor():
        while True:
            clear_screen()
            display_pet_and_menu()
            move_pet()
            time.sleep(0.5)  # Adjust the delay as desired for the pet's movement speed

# Execute the main function
if __name__ == "__main__":
    main()
