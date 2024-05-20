from abc import ABC, abstractmethod
import random
import pickle

class Character(ABC):
    def __init__(self, name):
        self._name = name
        self._attack = 0
        self._defense = 0
        self._experience = 0
        self._level = 1
        self._health = 100
        self._crit_chance = 0.1
        self._crit_damage = 1.5
        self._inventory = Inventory()
        self._equipped_items = EquippedItems()

    @property
    def name(self):
        return self._name

    @property
    def attack(self):
        return self._attack + self._equipped_items.attack_bonus

    @property
    def defense(self):
        return self._defense + self._equipped_items.defense_bonus

    @property
    def experience(self):
        return self._experience

    @property
    def level(self):
        return self._level

    @property
    def health(self):
        return self._health + self._equipped_items.health_bonus

    def receive_damage(self, damage):
        effective_damage = max(0, damage - self.defense)
        self._health -= effective_damage
        if self._health < 0:
            self._health = 0
        return effective_damage

    def calculate_attack(self):
        base_attack = self.attack
        if random.random() < self._crit_chance:
            base_attack *= self._crit_damage
        return base_attack

    def equip_item(self, item):
        self._equipped_items.equip_item(item)

    def unequip_item(self, item):
        self._equipped_items.unequip_item(item)

    @abstractmethod
    def level_up(self):
        pass

    def __str__(self):
        return (f"{self._name} (Level: {self._level})\n"
                f"Health: {self.health}\n"
                f"Attack: {self.attack}\n"
                f"Defense: {self.defense}\n"
                f"Experience: {self._experience}")

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack = 15
        self._defense = 10
        self._health = 120

    def level_up(self):
        self._level += 1
        self._attack += 3
        self._defense += 2
        self._health += 10

class Mage(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack = 20
        self._defense = 5
        self._health = 80

    def level_up(self):
        self._level += 1
        self._attack += 5
        self._defense += 1
        self._health += 5

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack = 18
        self._defense = 8
        self._health = 100

    def level_up(self):
        self._level += 1
        self._attack += 4
        self._defense += 2
        self._health += 8

class Paladin(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack = 13
        self._defense = 12
        self._health = 110

    def level_up(self):
        self._level += 1
        self._attack += 2
        self._defense += 3
        self._health += 12
class Item:
    def __init__(self, name, attack_bonus=0, defense_bonus=0, health_bonus=0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.health_bonus = health_bonus

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def __str__(self):
        return ', '.join([item.name for item in self.items])

class EquippedItems:
    def __init__(self):
        self.head = None
        self.left_hand = None
        self.right_hand = None
        self.body = None
        self.feet = None
        self.ring = None

    @property
    def attack_bonus(self):
        return sum(item.attack_bonus for item in self.items if item)

    @property
    def defense_bonus(self):
        return sum(item.defense_bonus for item in self.items if item)

    @property
    def health_bonus(self):
        return sum(item.health_bonus for item in self.items if item)

    @property
    def items(self):
        return [self.head, self.left_hand, self.right_hand, self.body, self.feet, self.ring]

    def equip_item(self, item):
        if isinstance(item, Item):
            if item.name == 'head':
                self.head = item
            elif item.name == 'left_hand':
                self.left_hand = item
            elif item.name == 'right_hand':
                self.right_hand = item
            elif item.name == 'body':
                self.body = item
            elif item.name == 'feet':
                self.feet = item
            elif item.name == 'ring':
                self.ring = item

    def unequip_item(self, item):
        if item == self.head:
            self.head = None
        elif item == self.left_hand:
            self.left_hand = None
        elif item == self.right_hand:
            self.right_hand = None
        elif item == self.body:
            self.body = None
        elif item == self.feet:
            self.feet = None
        elif item == self.ring:
            self.ring = None
class Game:
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

    def fight(self, char1, char2):
        print(f"Fight between {char1.name} and {char2.name}!")
        while char1.health > 0 and char2.health > 0:
            damage1 = char1.calculate_attack()
            damage2 = char2.calculate_attack()
            print(f"{char1.name} attacks {char2.name} for {damage1} damage!")
            char2.receive_damage(damage1)
            if char2.health <= 0:
                print(f"{char2.name} is defeated!")
                self.award_experience(char1, char2)
                break
            print(f"{char2.name} attacks {char1.name} for {damage2} damage!")
            char1.receive_damage(damage2)
            if char1.health <= 0:
                print(f"{char1.name} is defeated!")
                self.award_experience(char2, char1)
                break

    def award_experience(self, winner, loser):
        exp_gain = 10 * (loser.level / winner.level)
        winner._experience += exp_gain
        if winner._experience >= 100:
            winner.level_up()
            winner._experience -= 100
        print(f"{winner.name} gains {exp_gain} experience points.")

    def save_game(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_game(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

warrior = Warrior("Thor")
mage = Mage("Merlin")

game = Game()
game.add_character(warrior)
game.add_character(mage)

game.fight(warrior, mage)

game.save_game('savefile.pkl')
loaded_game = Game.load_game('savefile.pkl')

print(loaded_game.characters[0])
print(loaded_game.characters[1])

class Bot(Character):
    def __init__(self, name, level):
        super().__init__(name)
        self._level = level
        self._attack = 10 + (level * 2)
        self._defense = 5 + level
        self._health = 50 + (level * 5)

    def level_up(self):
        pass

def generate_bot(player_level):
    bot_level = random.randint(player_level - 1, player_level + 1)
    return Bot(f"Bot_Level_{bot_level}", bot_level)

class Forest:
    def __init__(self, player):
        self.player = player

    def adventure(self):
        while True:
            command = input("Enter 'fight' to encounter a bot or 'stop' to leave the forest: ").strip().lower()
            if command == 'stop':
                break
            elif command == 'fight':
                bot = generate_bot(self.player.level)
                game.fight(self.player, bot)
                if self.player.health <= 0:
                    print("You have been defeated!")
                    break
                if random.random() < 0.2:  # 20% chance to get an item
                    item = Item(f"Item_{random.randint(1, 100)}", attack_bonus=random.randint(1, 5))
                    self.player._inventory.add_item(item)
                    print(f"You found an item: {item.name}")
            else:
                print("Invalid command. Try again.")

player = Warrior("Conan")
forest = Forest(player)

forest.adventure()
