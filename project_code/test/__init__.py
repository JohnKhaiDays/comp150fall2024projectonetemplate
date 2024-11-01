import random

class Statistic:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def modify(self, amount):
        self.value += amount

class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.health = Statistic("Health", value=100)
        self.vitality = Statistic("Vitality", value=random.randint(1, 10))
        self.strength = Statistic("Strength", value=random.randint(1, 10))
        self.intelligence = Statistic("Intelligence", value=random.randint(1, 10))
        self.wisdom = Statistic("Wisdom", value=random.randint(1, 10))
        self.magic_power = Statistic("Magic Power", value=random.randint(1, 10))
        self.endurance = Statistic("Endurance", value=random.randint(1, 10))

    def attack(self, target):
        damage = random.randint(5, self.strength.value)
        target.health.modify(-damage)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        if target.health.value <= 0:
            print(f"{target.name} is dead!")

    def display_stats(self):
        print(f"{self.name}: Health = {self.health.value}, Vitality = {self.vitality.value}, "
              f"Strength = {self.strength.value}, Intelligence = {self.intelligence.value}, "
              f"Wisdom = {self.wisdom.value}, Magic Power = {self.magic_power.value}, "
              f"Endurance = {self.endurance.value}")

class Event:
    def __init__(self, prompt, skill_check_stat, pass_message, fail_message):
        self.prompt = prompt
        self.skill_check_stat = skill_check_stat
        self.pass_message = pass_message
        self.fail_message = fail_message

    def encounter(self, character):
        print(self.prompt)
        check_value = random.randint(1, 20) + character.__dict__[self.skill_check_stat].value
        print(f"Check result: {check_value} (Skill: {character.__dict__[self.skill_check_stat].value})")
        
        if check_value >= 18:
            print(f"Critical success! {self.pass_message}")
        elif check_value >= 15:
            print(self.pass_message)
        elif check_value >= 10:
            print(f"Partial success: You manage to accomplish part of the task, but face some challenges.")
        else:
            print(self.fail_message)

class Party:
    def __init__(self):
        self.members = []

    def add_member(self, character):
        self.members.append(character)
        print(f"{character.name} has joined the party!")

    def display_members(self):
        print("Party Members:")
        for member in self.members:
            member.display_stats()

# Main game loop
def main():
    print("Welcome to the Fantasy Quest!")
    
    party = Party()
    
    # Create initial party member
    player_name = input("Enter your character's name: ")
    character_class = input("Choose your class (Warrior/Mage): ")
    player = Character(player_name, character_class)
    party.add_member(player)

    # Allow adding more party members
    while True:
        add_member = input("Do you want to add another party member? (yes/no): ").strip().lower()
        if add_member == 'yes':
            name = input("Enter the new member's name: ")
            char_class = input("Choose class (Warrior/Mage): ")
            new_member = Character(name, char_class)
            party.add_member(new_member)
        elif add_member == 'no':
            break
        else:
            print("Please answer with 'yes' or 'no'.")

    enemy = Character("Dark Wizard", "Villain")

    # Game loop
    while any(member.health.value > 0 for member in party.members) and enemy.health.value > 0:
        party.display_members()
        
        print("\nActions:")
        print("1. Attack")
        print("2. Encounter a random event")
        choice = input("What do you want to do? (1/2): ")
        
        if choice == '1':
            for member in party.members:
                if member.health.value > 0:
                    member.attack(enemy)
                    enemy.display_stats()  # Show enemy stats after attack
                    if enemy.health.value <= 0:
                        print(f"{enemy.name} has been defeated! You win!")
                        return
            
            # Enemy attacks back
            for member in party.members:
                if member.health.value > 0:
                    enemy.attack(member)
                    member.display_stats()  # Show player stats after enemy attack
                    if member.health.value <= 0:
                        print(f"{member.name} has been defeated.")
        
        elif choice == '2':
            # Randomly generate an event
            random_events = [
                Event(
                    prompt="You encounter a magical creature that needs help!",
                    skill_check_stat='intelligence',
                    pass_message="You successfully help the creature, gaining its favor!",
                    fail_message="The creature misunderstands your intentions and becomes hostile!"
                ),
                Event(
                    prompt="You find a heavy boulder blocking your path!",
                    skill_check_stat='strength',
                    pass_message="You manage to lift the boulder and clear the way!",
                    fail_message="The boulder is too heavy, and you injure yourself in the attempt!"
                ),
                Event(
                    prompt="A wise old sage offers you a riddle to solve.",
                    skill_check_stat='wisdom',
                    pass_message="You solve the riddle and earn valuable knowledge!",
                    fail_message="You fail to solve the riddle and lose some time."
                )
            ]
            random_event = random.choice(random_events)
            for member in party.members:
                if member.health.value > 0:
                    random_event.encounter(member)  # Use the party member for the event
            
            # After the event, enemy attacks back
            if enemy.health.value > 0:  # Only attack if the enemy is still alive
                for member in party.members:
                    if member.health.value > 0:
                        enemy.attack(member)
                        member.display_stats()  # Show player stats after enemy attack
                        if member.health.value <= 0:
                            print(f"{member.name} has been defeated.")

if __name__ == "__main__":
    main()