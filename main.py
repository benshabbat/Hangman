from hangman.game import *
from hangman.io import *
from hangman.words import choose_secret_word
from data.word_data import WORDS_DATA

def play(words: list[str], max_tries: int = 6) -> None:
    secret_word = choose_secret_word(words)
    state = init_state(secret_word, max_tries)
    while not is_won(state) and not is_lost(state):
        guess = prompt_guess()
        if validate_guess(guess, state["guessed"])[0]:
            apply_guess(state, guess)
        # apply_guess(state, guess)
        print_result(state)
        
if __name__ == "__main__":
    play(WORDS_DATA)        