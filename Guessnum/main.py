import random

num = random.randint(1, 100)
print("Welcome to the Guess the Number Game!")
while True:
    try:
        guess = int(input("Please enter your guess (between 1 and 100): "))
        if guess < num:
            print("Too low! Try again.")
        elif guess > num:
            print("Too high! Try again.")
        else:
            print("Congratulations! You've guessed the number!")
            break
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 100.")

    