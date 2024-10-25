from helpers import (
    exit_program,
    list_meals,
    find_meal_by_name,
    find_meal_by_id,
    create_meal,
    update_meal,
    delete_meal,
    list_recipes,
    find_recipe_by_name,
    find_recipe_by_id,
    create_recipe,
    update_recipe,
    delete_recipe,
    list_meal_recipes
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_meals()
        elif choice == "2":
            find_meal_by_name()
        elif choice == "3":
            find_meal_by_id()
        elif choice == "4":
            create_meal()
        elif choice == "5":
            update_meal()
        elif choice == "6":
            delete_meal()
        elif choice == "7":
            list_recipes()
        elif choice == "8":
            find_recipe_by_name()
        elif choice == "9":
            find_recipe_by_id()
        elif choice == "10":
            create_recipe()
        elif choice == "11":
            update_recipe()
        elif choice == "12":
            delete_recipe()
        elif choice == "13":
            list_meal_recipes()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all meals")
    print("2. Find meal by name")
    print("3. Find meal by id")
    print("4: Create meal")
    print("5: Update meal")
    print("6: Delete meal")
    print("7. List all recipes")
    print("8. Find recipe by name")
    print("9. Find recipe by id")
    print("10: Create recipe")
    print("11: Update recipe")
    print("12: Delete recipe")
    print("13: List all recipes in a meal")


if __name__ == "__main__":
    main()
