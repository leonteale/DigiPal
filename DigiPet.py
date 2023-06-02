# (Imports, ASCII art, DATA_FILE, get_key, and DigiPet class definition)

import datetime

# ASCII Art for the DigiPet
grave = """
_______
| RIP |
|     |
|     |
|     |
|_____| 
"""

# Initialize the attributes of the DigiPet
class DigiPet:
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
        # Check if the pet is dead
        if self.hunger <= 0 and (self.death_time is None or (datetime.datetime.now() - self.death_time).total_seconds() >= 5 * 60):
            self.status = 'Dead'
            return
        elif self.hunger <= 0 and self.death_time is None:
            self.death_time = datetime.datetime.now()

        # Randomly move the pet
        new_position = [random.randint(0, self.boundary[0]), random.randint(0, self.boundary[1])]
        if 0 <= new_position[0] < self.boundary[0] and 0 <= new_position[1] < self.boundary[1]:
            self.position = new_position

        # Randomly decrease the hunger level
        if (datetime.datetime.now() - self.last_activity).total_seconds() >= random.randint(1, 5) * 60:
            self.hunger = max(0, self.hunger - random.randint(1, 5))
            self.last_activity = datetime.datetime.now()

        # Update the feelings of the pet based on the hunger level
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

def draw_border(pet):
    # Calculate the pet's boundary relative to the terminal size
    pet.boundary = [pet.terminal_size[0] - 2, pet.terminal_size[1]//2 - 2]

    # Draw the boundary with a white background
    print('\033[47m' + ' ' * (pet.boundary[0] + 2) + '\033[0m')  # Top border
    for _ in range(pet.boundary[1]):
        print('\033[47m' + ' ' + '\033[0m' + ' ' * pet.boundary[0] + '\033[47m' + ' ' + '\033[0m')  # Side borders
    print('\033[47m' + ' ' * (pet.boundary[0] + 2) + '\033[0m')  # Bottom border

def display_quick_stats(pet):
    print(f'\n\nName: {pet.name} | Hunger: {pet.hunger} | Feelings: {pet.feelings} | Status: {pet.status}\n\n')

if __name__ == "__main__":
    # (Signal handling, loading pet data, main loop)
