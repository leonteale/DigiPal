#!/usr/bin/env python

from blessed import Terminal

# Define the pet's ASCII art representation
pet_ascii = r"""
   /\_/\
 ( o.o )
 > ^ <
"""

# Initialize the terminal
term = Terminal()

# Function to clear the terminal screen
def clear_screen():
    print(term.clear)

# Function to display the pet
def display_pet(pet_x, pet_y):
    # Draw the pet
    lines = pet_ascii.strip().split('\n')
    for i, line in enumerate(lines):
        print(term.move_xy(pet_x, pet_y + i) + line)
