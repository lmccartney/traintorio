import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Item:
    name: str
    stack_size: int
    recipe: Optional['Recipe'] = None


@dataclass
class Recipe:
    ingredients: list['IngredientInformation']

    @property
    def is_optimized(self):
        return all([self.car_is_fully_packed, self.item_ratios_are_good])

    @property
    def item_ratios_are_good(self):
        for ingredient in self.ingredients:
            if not self.ingredient_ratio(ingredient) == self.item_count_ratio(ingredient):
                return False
        return True

    @property
    def car_is_fully_packed(self):
        return self.minimum_stacks > self.available_car_slots

    @property
    def available_car_slots(self):
        return 40 - sum([x.stacks for x in self.ingredients])

    @property
    def total_items_in_recipe(self):
        return sum([x.number for x in self.ingredients])

    @property
    def total_items_in_car(self):
        return sum([x.stacks * x.item.stack_size for x in self.ingredients])

    @property
    def minimum_stacks(self):
        return sum([x.minimum_stack for x in self.ingredients])

    def ingredient_ratio(self, ingredient: 'IngredientInformation'):
        return ingredient.number / self.total_items_in_recipe

    def item_count_ratio(self, ingredient: 'IngredientInformation'):
        if self.total_items_in_car == 0:
            return -1
        return ingredient.total_items_in_car / self.total_items_in_car


@dataclass
class IngredientInformation:
    item: 'Item'
    number: int
    stacks: int = 0
    minimum_stack: Optional[int] = None

    @property
    def minimum_count(self):
        return self.item.stack_size * self.number

    @property
    def total_items_in_car(self):
        return self.stacks * self.item.stack_size


def run():
    iron_ore = Item('Iron Ore', 50)
    copper_ore = Item('Copper Ore', 50)
    iron_plate = Item('Iron Plate', 100, Recipe([IngredientInformation(iron_ore, 1)]))
    copper_plate = Item('Copper Plate', 100, Recipe([IngredientInformation(copper_ore, 1)]))
    copper_cable = Item('Copper Cable', 200, Recipe([IngredientInformation(copper_plate, 1)]))
    electronic_circuit = Item('Electronic Circuit', 200, Recipe([IngredientInformation(iron_plate, 1), IngredientInformation(copper_cable, 3)]))
    optimize_train_car(electronic_circuit)
    print_car_info(electronic_circuit)


def optimize_train_car(item: Item):
    if not item.recipe:
        return
    item.recipe.ingredients = sorted(item.recipe.ingredients, key=lambda x: x.minimum_count)
    while not item.recipe.item_ratios_are_good:
        for ingredient in item.recipe.ingredients:
            if item.recipe.ingredient_ratio(ingredient) > item.recipe.item_count_ratio(ingredient):
                ingredient.stacks += 1
        if item.recipe.available_car_slots < 0:
            raise Exception('Car ran out of slots! bad!')
    for ingredient in item.recipe.ingredients:
        ingredient.minimum_stack = ingredient.stacks
    while not item.recipe.car_is_fully_packed:
        if item.recipe.minimum_stacks <= item.recipe.available_car_slots:
            for ingredient in item.recipe.ingredients:
                ingredient.stacks += ingredient.minimum_stack


def print_car_info(item: Item):
    for ingredient in item.recipe.ingredients:
        print(f'{ingredient.item.name}: {ingredient.stacks}')

if __name__ == '__main__':
    run()
