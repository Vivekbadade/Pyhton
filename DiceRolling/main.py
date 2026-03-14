import random
choice=True

while choice:
    print("Do you want to roll the dice? (y/n)")
    user_input=input()
    if user_input.lower()=='y':
        dice1_roll=random.randint(1,6)
        dice2_roll=random.randint(1,6)
        print(f"You rolled a ( {dice1_roll} ),( {dice2_roll} ) !")
    elif user_input.lower()=='n':
        print("Thanks for playing!")
        choice=False
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
