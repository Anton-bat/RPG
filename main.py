from abc import ABC, abstractmethod
import random
import pickle

class Charachter(ABC):
    def __init__(self, name) -> None:
        self._name = name
        self._attack = 0
        self._defence = 0
        self._experience = 0
        self._level = 1
        self._health = 100
        self._critic_damage = 1.5
        self._percent_of_critic_damage = 0.1
        self._inventory = Inventory()
        self._weared_items = WearedItems()
    
    @property
    def name(self):
        return self._name
    
    @property
    def attack(self):
        return self._attack + self._weared_items.add_attack
    
    @property
    def defence(self):
        return self._defence + self._weared_items.add_defence
    
    @property
    def experience(self):
        return self._experience
    
    @property
    def level(self):
        return self._level
    
    @property
    def health(self):
        return self._health + self._weared_items.add_health
    
    def calculate_damage(self, damage):
        received_damage = max(0, damage - self.defence)
        self._health -= received_damage
        if self._health < 0:
            self._health = 0
        return received_damage
    
    def calculate_attack(self):
        base_attack = self.attack
        if random.random() < self._percent_of_critic_damage:
            base_attack *= self._critic_damage
        return base_attack
    
    def wear_items(self, item):
        self._weared_items.wear_item(item)
    
    def unwear_item(self, item):
        self._weared_items.unwear_item(item)
    
    @abstractmethod
    def level_up(self):
        pass

    def __str__(self) -> str:
        return (f'{self._name}, Level: {self._level}\n'
                f'Health: {self._health}\n'
                f'Defence: {self._defence}\n'
                f'Attack: {self._attack}\n'
                f'Experience: {self._experience}')
    
    


