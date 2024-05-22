from abc import ABC, abstractmethod
import random
import pickle

class Character(ABC):
    def __init__(self, name) -> None:
        self._name = name
        self._attack = 0
        self._defence = 0
        self._experience = 0
        self._level = 1
        self._health = 100
        self._crit_chance = 0.1
        self._crit_hit = 0.1
        self._inventory = Inventory()
        self._equiped_items = EquipedItems()

    @property
    def name(self):
        return self._name
    
    @property
    def attack(self):
        return self._attack + self._equiped_items.attack_bonus
    
    @property
    def defence(self):
        return self._defence + self._equiped_items.defence_bonus
    
    @property
    def experience(self):
        return self._experience
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        self._level = value

    
    @property
    def health(self):
        return self._health + self._equiped_items.health_bonus

    def calculate_attack(self):
        base_attack = self._attack
        if random.random() < self._crit_chance:
            base_attack *= self._crit_hit
        return base_attack

    def calculate_damage(self, damage):
        received_damage = max(0, damage - self._defence)
        self._health -= received_damage
        if self._health <= 0 :
            self._health = 0
        return received_damage
    
    @abstractmethod
    def level_up(self):
        pass

    def equiped_items(self, item):
        return self._equiped_items.equip_item(item)
    
    def unequiped_items(self, item):
        return self._equiped_items.unequip_item(item)
    
    def __str__(self):
        return (f"{self._name} (Level: {self._level})\n"
                f"Health: {self.health}\n"
                f"Attack: {self.attack}\n"
                f"Defense: {self.defence}\n"
                f"Experience: {self._experience}")

class Warrior(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._attack = 15
        self._health = 100
        self._defence = 10
    
    def level_up(self):
        self._level += 1
        self._attack += 3
        self._health += 10
        self._defence += 2

class Rogue(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._attack = 15
        self._health = 90
        self._defence = 8
    
    def level_up(self):
        self._level += 1
        self._attack += 3
        self._health += 7
        self._defence += 2

class Paladin(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._attack = 14
        self._health = 110
        self._defence = 12
    
    def level_up(self):
        self._level += 1
        self._attack += 3
        self._health += 11
        self._defence += 4

class Mage(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self._attack = 20
        self._health = 80
        self._defence = 5
    
    def level_up(self):
        self._level += 1
        self._attack += 2
        self._health += 8
        self._defence += 3

class Inventory:
    def __init__(self) -> None:
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def __str__(self) -> str:
        return ", ".join([item.name for item in self.items])

class Item:
    def __init__(self, name, item_type, attack_bonus = 0, defence_bonus = 0, health_bonus = 0) -> None:
        self.name = name
        self.item_type = item_type
        self.attack_bonus = attack_bonus
        self.defence_bonus = defence_bonus
        self.health_bonus = health_bonus

class EquipedItems:
    def __init__(self) -> None:
        self.head = None
        self.right_hand = None
        self.left_hand = None
        self.body = None
        self.feet = None
        self.ring = None

    @property
    def attack_bonus(self):
        return sum(item.attack_bonus for item in self.items if item)
    
    @property
    def defence_bonus(self):
        return sum(item.defence_bonus for item in self.items if item)

    @property
    def health_bonus(self):
        return sum(item.health_bonus for item in self.items if item)

    @property
    def items(self) -> str:
        return [self.head, self.left_hand, self.right_hand, self.body, self.feet, self.ring] 
    
    def equip_item(self, item):
        if isinstance(item, Item):
            if item.item_type == "head":
                self.head == item
            elif item.item_type == "right_hand":
                self.right_hand == item
            elif item.item_type == "left_hand":
                self.left_hand == item
            elif item.item_type == "body":
                self.body == item
            elif item.item_type == "feet":
                self.feet == item
            elif item.item_type == "ring":
                self.ring == item

    def unequip_item(self, item):
        if item == self.head:
            self.head == None
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
    def __init__(self) -> None:
        self.characters = []
    
    def add_character(self, character):
        self.characters.append(character)
    
    def fight(self, char1, char2):
        print(f'Fight between {char1} and {char2} has began')
        while char1.health > 0 and char2.health > 0:
            damage1 = char1.calculate_attack()
            damage2 = char2.calculate_attack()
            print(f'{char1} hits {char2} with {damage1}')
            char2.calculate_damage(damage1)
            if char2.health <= 0:
                print(f'{char2.name} is dead')
                self.award_experience(char1, char2)
                break
            print(f'{char2} hits {char1} with {damage2}')
            char1.calculate_damage(damage2)
            if char1.health <= 0:
                print(f'{char1.name} is dead')
                self.award_experience(char2, char1)
                break
    
    def award_experience(self, winner, loser):
        base_exp_gain = 30
        gain_exp = base_exp_gain * (loser.level / winner.level)
        winner._experience += gain_exp
        if winner._experience >= 100:
            winner.level_up()
            winner._experience -= 100
        print(f'{winner.name} has earned {gain_exp} experience.')
    
    def save_game(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_game(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

class Bot(Character):
    def __init__(self, name, level) -> None:
        super().__init__(name)
        self.level = level
        self._attack = 5 + (level * 2)
        self._defence = 2 + (level * 2)
        self._health = 50 + (level * 4)
    
    def level_up(self):
        pass


def generate_bot(player_level):
        bot_level = random.randint(player_level - 1, player_level + 1)
        return Bot(f"Bot_with_level{bot_level}", bot_level)

def generate_random_item():
    name = f"Item_{random.randint(1, 100)}"
    attack_bonus = random.randint(0, 5)
    defense_bonus = random.randint(0, 5)
    health_bonus = random.randint(0, 5)
    return Item(name, attack_bonus, defense_bonus, health_bonus)

def generate_three_items():
    return [generate_random_item() for _ in range(3)]

def choose_random_item(items):
    return random.choice(items)

class Forest:
    def __init__(self, player) -> None:
        self.player = player
        self.game = Game()
        self.game.add_character(player)
    
    def adventure(self):
        while True:
            command = input("Enter 'fight' to encounter a bot or 'stop' to leave the forest: ").strip().lower()
            if command == 'stop':
                break
            elif command == 'fight':
                bot = generate_bot(self.player.level)
                self.game.fight(self.player, bot)
                if self.player.health <= 0:
                    print('You are dead')
                    break
                if random.random() < 0.2:
                    items = generate_random_item()
                    item = choose_random_item(items)
                    self.player._inventory.add_item(item)
                    print(f'You found item: {item}')
            else:
                print("Invalid command. Try again.")

player = Warrior("Conan")
forest = Forest(player)
forest.adventure()