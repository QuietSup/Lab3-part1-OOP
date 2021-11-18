import calendar
import json
import os
from datetime import datetime

# Pizzeria offers pizza-of-the-day for business lunch. The type of
# pizza-of-the-day depends on the day of week. Having a pizza-of-the-day
# simplifies ordering for customers. They don't have to be experts on
# specific types of pizza. Also, customers can add extra ingredients to
# the pizza-of-the-day. Write a program that will form orders from customers.


class Pizza:
    """Contains info about general pizza, its name, ingredients and menu file name"""
    def __init__(self, name, ingredients: list):
        self._name = name
        self.__ingredients = ingredients
        self._file_name = 'menu.json'

    def add_smth(self, extra_ingredients: list):
        """To add ingredients to pizza order"""
        if not extra_ingredients:
            raise ValueError('No data was entered')
        if not isinstance(extra_ingredients, list):
            raise TypeError('item(s) to add must be passed as list')
        self.ingredients.extend(extra_ingredients)

    def remove_smth(self, away: list):
        """Remove ingredients from pizza order"""
        if not away:
            raise ValueError('No data was entered')
        if not isinstance(away, list):
            raise TypeError('item(s) to remove must be passed as list')
        self.ingredients = list(set(self.ingredients) - set(away))

    def save(self):
        """Save all order (with changes if they exist) to the .json file with menu"""
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w'):
                pass

        if os.path.getsize(self.file_name):
            with open(self.file_name, "r") as read_file:
                saved_pizzas = json.load(read_file)

            saved_pizzas[self.name] = self.ingredients

            with open(self.file_name, "w") as write_file:
                json.dump(saved_pizzas, write_file, indent=4)

        else:
            with open(self.file_name, "w") as write_file:
                json.dump({self.name: self.ingredients}, write_file, indent=4)

    @property
    def name(self):
        return self._name

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def file_name(self):
        return self._file_name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Name must be str type')
        if value in calendar.day_name:
            raise ValueError(f'{value} must be pizza-of-the-day (Potd class)')
        self._name = value

    @ingredients.setter
    def ingredients(self, value):
        if not isinstance(value, list):
            raise TypeError('Ingredients must be list type')
        self.__ingredients = value

    @file_name.setter
    def file_name(self, value):
        if not isinstance(value, str):
            raise TypeError('File_name must be str')
        if not value.endswith('.json'):
            raise TypeError('File must be .json type')
        self._file_name = value


class Potd(Pizza):
    """Contains info about pizza-of-the-day depending on a day of week

    Saves info to .json file containing pizza-of-the-day menu
    """
    def __init__(self, ingredients: list):
        super().__init__(datetime.today().strftime('%A'), ingredients)
        self._file_name = 'pizza-of-the-day.json'

    @Pizza.name.setter
    def name(self, value):
        if value not in calendar.day_name:
            raise ValueError('pizza-of-the-day must have a name of a week day')
        self._name = value


def remove_from_menu(name):
    """Remove some pizza from general menu"""
    if not name:
        raise ValueError('No data as a pizza name')
    if not isinstance(name, str):
        raise TypeError('Pizza name must be str type')

    file_name = 'menu.json'

    if not os.path.exists(file_name):
        raise FileNotFoundError("Menu file doesn't exist")

    if os.path.getsize(file_name):
        with open(file_name, "r") as read_file:
            saved_pizzas = json.load(read_file)

        if name in list(saved_pizzas.keys()):
            saved_pizzas.pop(name)

        else:
            raise ValueError(f'{name} doesn\'t exist in this pizza')

        with open(file_name, "w") as write_file:
            json.dump(saved_pizzas, write_file, indent=4)

    else:
        raise ValueError("File is empty")


def show_menu():
    """Shows menu including pizza-of-the-day"""
    menu_file = 'menu.json'
    potd_file = 'pizza-of-the-day.json'

    if not os.path.exists(menu_file):
        raise OSError(f'{menu_file} doesn\'t exist')

    if not os.path.exists(potd_file):
        raise OSError(f'{potd_file} doesn\'t exist')

    if os.path.getsize(menu_file):
        with open(menu_file, "r") as read_file:
            menu = json.load(read_file)
    else:
        raise ValueError("File is empty")

    if os.path.getsize(potd_file):
        with open(potd_file, "r") as read_file:
            potd = json.load(read_file)
            today = datetime.today().strftime('%A')
            if today in list(potd.keys()):
                menu.update({today: potd[today]})
    else:
        raise ValueError("File is empty")

    return menu


x = Pizza('Quattro', ['tomato', 'mushrooms'])
# x.name = 'Wednesday'
x.save()
y = Potd(['tomato', 'speck'])
y.add_smth(['mozzarella', 'gorgonzola'])
y.remove_smth(['gorgonzola', 'speck'])
#y.name = 'Wednesday'
y.save()
print(show_menu())
# remove_from_menu('Margarita')

