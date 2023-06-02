#!/usr/bin/env python

import os
import datetime

# Function to get user input for pet name
def get_pet_name():
    pet_name = input("Enter a name for your pet: ")
    return pet_name

# Function to initialize the pet and store the data
def initialize_pet():
    pet_name = get_pet_name()
    pet_birthday = datetime.datetime.now().strftime("%Y-%m-%d")

    # Create the data directory if it doesn't exist
    data_dir = os.path.expanduser("~/.Digipet")
    os.makedirs(data_dir, exist_ok=True)

    # Write the pet's data to a file
    data_file = os.path.join(data_dir, "data.txt")
    with open(data_file, "w") as file:
        file.write(f"Name: {pet_name}\n")
        file.write(f"Birthday: {pet_birthday}")

# Execute the initialization function
if __name__ == "__main__":
    initialize_pet()
