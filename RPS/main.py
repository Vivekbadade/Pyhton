import random


choices = ("r", "p", "s")
play=True

def get_user_choice():
    while True:
        userinput = input("Rock, Paper or Scissors? (r/p/s): ").lower()
        if userinput in choices:
            return userinput
        else:
            print("Invalid input. Please choose 'r', 'p', or 's'.")
            

def winner(userinput, computer_choice):
    if userinput == computer_choice:
        return "It's a tie!"
    elif (userinput == "r" and computer_choice == "s") or (userinput == "p" and computer_choice == "r") or (userinput == "s" and computer_choice == "p"):
        return "You win!"
    else:
        return "Computer wins!"

while play:
    userinput = get_user_choice()

    computer_choice = random.choice(choices)

    print(winner(userinput, computer_choice))
    
    play_again = input("Do you want to play again? (y/n): ")
    if play_again.lower() != "y":
        play = False
        print("Thanks for playing!")
        break