#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.meal import Meal
from models.recipe import Recipe

def seed_database():
    Recipe.drop_table()
    Meal.drop_table()
    Meal.create_table()
    Recipe.create_table()

    # Create seed data
    payroll = Meal.create("Payroll")
    human_resources = Meal.create("Human Resources")
    
    Recipe.create("Amir", "Accountant", payroll.id)
    Recipe.create("Bola", "Manager", payroll.id)
    Recipe.create("Charlie", "Manager", human_resources.id)
    Recipe.create("Dani", "Benefits Coordinator", human_resources.id)
    Recipe.create("Hao", "New Hires Coordinator", human_resources.id)


seed_database()
print("Seeded database")
