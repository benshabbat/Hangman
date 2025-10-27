from hangman.game import *


def prompt_guess() -> str:
    return input("Enter your guess: ").strip()


def print_status(state: dict) -> None:
    print(render_display(state))
    print(render_summary(state))



def print_result(state: dict) -> None:
    if is_won(state):
        print("Congratulations! You've won!")
        print_status(state)

    elif is_lost(state):
        print(f"Game over! The secret word was: {state['secret']}")
        print_status(state)

    else:
        print("Keep guessing!")

    print(render_display(state))