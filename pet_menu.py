#!/usr/bin/env python

from blessed import Terminal

# Initialize the terminal
term = Terminal()

# Function to clear the terminal screen
def clear_screen():
    print(term.clear)

# Function to display the menu
def display_menu(box_height):
    menu_text = "Menu: 1. Info  |  2. Feed  |  3. Play  |  4. Exit"
    with term.location(0, box_height):
        print(term.black_on_white(menu_text))
