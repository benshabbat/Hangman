def init_state(secret: str, max_tries: int) -> dict:
    guessed = set() 
    display = ["_"] * len(secret)
    wrong_guesses = 0
    return {
        "secret": secret,
        "display": display,
        "guessed": guessed,
        "wrong_guesses": wrong_guesses,
        "max_tries": max_tries,
    }



def validate_guess(ch: str, guessed: set[str]) -> tuple[bool, str]:
    if len(ch) != 1 or not ch.isalpha():
        return False, "Please enter a single alphabetical character."
    ch = ch.lower()
    if ch in guessed:
        return False, f"You have already guessed '{ch}'. Try a different letter."
    return True, ""

def apply_guess(state: dict, ch: str) -> bool:
    ch = ch.lower()
    state["guessed"].add(ch)
    if ch in state["secret"]:
        for idx, letter in enumerate(state["secret"]):
            if letter == ch:
                state["display"][idx] = ch
        return True
    state["wrong_guesses"] += 1
    return False

def apply_guess(state: dict, ch: str) -> bool:
    is_valid, msg = validate_guess(ch,state["guessed"])
    if is_valid:
        ch = ch.lower()
        state["guessed"].add(ch)
        if ch in state["secret"]:
            for idx, letter in enumerate(state["secret"]):
                if letter == ch:
                    state["display"][idx] = ch
            return True
        state["wrong_guesses"] += 1
    return False



def is_won(state: dict) -> bool:
    return "_" not in state["display"]

def is_lost(state: dict) -> bool:
    return state["wrong_guesses"] >= state["max_tries"]

def render_display(state: dict) -> str:
    return " ".join(state["display"])


def render_summary(state: dict) -> str:
    return (
        f"Guessed letters: {', '.join(sorted(state['guessed']))}\n"
        f"Wrong guesses: {state['wrong_guesses']} / {state['max_tries']}"
    )
    
    