from models.meal import Meal
from models.recipe import Recipe

def exit_program():
    print("Goodbye!")
    exit()

# We'll implement the meal functions in this lesson


def list_meals():
    meals = Meal.get_all()
    for meal in meals:
        print(meal)


def find_meal_by_name():
    name = input("Enter the meal's name: ")
    meal = Meal.find_by_name(name)
    print(meal) if meal else print(
        f'Meal {name} not found')


def find_meal_by_id():
    # use a trailing underscore not to override the built-in id function
    id_ = input("Enter the meal's id: ")
    meal = Meal.find_by_id(id_)
    print(meal) if meal else print(f'Meal {id_} not found')


def create_meal():
    name = input("Enter the meal's name: ")
    try:
        meal = Meal.create(name)
        print(f'Success: {meal}')
    except Exception as exc:
        print("Error creating meal: ", exc)


def update_meal():
    id_ = input("Enter the meal's id: ")
    if meal := Meal.find_by_id(id_):
        try:
            name = input("Enter the meal's new name: ")
            meal.name = name

            meal.update()
            print(f'Success: {meal}')
        except Exception as exc:
            print("Error updating meal: ", exc)
    else:
        print(f'Meal {id_} not found')


def delete_meal():
    id_ = input("Enter the meal's id: ")
    if meal := Meal.find_by_id(id_):
        meal.delete()
        print(f'Meal {id_} deleted')
    else:
        print(f'Meal {id_} not found')


# You'll implement the recipe functions in the lab

def list_recipes():
    recipes = Recipe.get_all()
    for recipe in recipes:
        print(recipe)


def find_recipe_by_name():
    name = input("Enter the recipe's name: ")
    recipe = Recipe.find_by_name(name)
    print(recipe) if recipe else print(
        f'Recipe {name} not found')


def find_recipe_by_id():
    id_ = input("Enter the recipe's id: ")
    recipe = Recipe.find_by_id(id_)
    print(recipe) if recipe else print(f'Recipe {id_} not found')


def create_recipe():
    name = input("Enter the recipe's name: ")
    category = input("Enter the recipe's category: ")
    meal_id = input("Enter the recipe's meal id:")
    try:
        recipe = Recipe.create(name, category, meal_id)
        print(f'Success: {recipe}')
    except Exception as exc:
        print("Error creating recipe: ", exc)


def update_recipe():
    id_ = input("Enter the recipe's id: ")
    if recipe := Recipe.find_by_id(id_):
        try:
            name = input("Enter the recipes's new name: ")
            recipe.name = name
            category = input("Enter the recipe's new category:")
            recipe.category = category
            meal_id = input("Enter the recipes's new meal id: ")
            recipe.meal_id = meal_id
            recipe.update()
            print(f'Success: {recipe}')
        except Exception as exc:
            print("Error updating recipe: ", exc)
    else:
        print(f'Recipe {id_} not found')


def delete_recipe():
    id_ = input("Enter the recipe's id: ")
    if recipe := Recipe.find_by_id(id_):
        recipe.delete()
        print(f'Recipe {id_} deleted')
    else:
        print(f'Recipe {id_} not found')


def list_meal_recipes():
    id_ = input("Enter the meal's id: ")
    if meal := Meal.find_by_id(id_):
        for recipe in meal.recipes():
            print(recipe)
    else:
        print(f'Meal {id_} not found')