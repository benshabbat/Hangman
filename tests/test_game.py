import unittest
import sys
import os

# Add project directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hangman.game import init_state, validate_guess, apply_guess, is_won, is_lost, render_display, render_summary
from hangman.words import choose_secret_word


class TestHangmanGame(unittest.TestCase):
    """Simple tests for Hangman game"""

    def test_init_state_creates_correct_game(self):
        """Test that initial state is created correctly"""
        # Test with word "cat" and 3 tries
        state = init_state("cat", 3)
        
        self.assertEqual(state["secret"], "cat")
        self.assertEqual(state["display"], ["_", "_", "_"])
        self.assertEqual(state["guessed"], set())
        self.assertEqual(state["wrong_guesses"], 0)
        self.assertEqual(state["max_tries"], 3)

    def test_validate_guess_good_letter(self):
        """Test that valid letter passes validation"""
        guessed = set()
        is_valid, message = validate_guess("a", guessed)
        
        self.assertTrue(is_valid)
        self.assertEqual(message, "")

    def test_validate_guess_already_guessed(self):
        """Test that already guessed letter is rejected"""
        guessed = {"a", "b"}
        is_valid, message = validate_guess("a", guessed)
        
        self.assertFalse(is_valid)
        self.assertIn("already guessed", message)

    def test_validate_guess_not_letter(self):
        """Test that numbers or symbols are rejected"""
        guessed = set()
        is_valid, message = validate_guess("1", guessed)
        
        self.assertFalse(is_valid)
        self.assertIn("alphabetical character", message)

    def test_apply_guess_correct_letter(self):
        """Test that correct guess works"""
        state = init_state("cat", 3)
        result = apply_guess(state, "c")
        
        self.assertTrue(result)  # Guess is correct
        self.assertEqual(state["display"], ["c", "_", "_"])
        self.assertIn("c", state["guessed"])
        self.assertEqual(state["wrong_guesses"], 0)

    def test_apply_guess_wrong_letter(self):
        """Test that wrong guess works"""
        state = init_state("cat", 3)
        result = apply_guess(state, "x")
        
        self.assertFalse(result)  # Guess is wrong
        self.assertEqual(state["display"], ["_", "_", "_"])
        self.assertIn("x", state["guessed"])
        self.assertEqual(state["wrong_guesses"], 1)

    def test_is_won_true(self):
        """Test that win detection works"""
        state = init_state("cat", 3)
        state["display"] = ["c", "a", "t"]  # All letters guessed
        
        self.assertTrue(is_won(state))

    def test_is_won_false(self):
        """Test that win detection works when letters remain"""
        state = init_state("cat", 3)
        state["display"] = ["c", "_", "t"]  # Still has letters to guess
        
        self.assertFalse(is_won(state))

    def test_is_lost_true(self):
        """Test that loss detection works"""
        state = init_state("cat", 3)
        state["wrong_guesses"] = 3  # Reached maximum tries
        
        self.assertTrue(is_lost(state))

    def test_is_lost_false(self):
        """Test that loss detection works when tries remain"""
        state = init_state("cat", 3)
        state["wrong_guesses"] = 2  # Still has tries left
        
        self.assertFalse(is_lost(state))

    def test_render_display(self):
        """Test that display rendering works"""
        state = init_state("cat", 3)
        state["display"] = ["c", "_", "t"]
        
        result = render_display(state)
        self.assertEqual(result, "c _ t")

    def test_render_summary(self):
        """Test that summary rendering works"""
        state = init_state("cat", 3)
        state["guessed"] = {"c", "x", "a"}
        state["wrong_guesses"] = 1
        
        result = render_summary(state)
        self.assertIn("a, c, x", result)  # Letters sorted
        self.assertIn("1 / 3", result)    # Wrong guesses

    def test_choose_secret_word(self):
        """Test that word selection works"""
        words = ["cat", "dog", "bird"]
        chosen_word = choose_secret_word(words)
        
        self.assertIn(chosen_word, words)

    def test_full_game_scenario_win(self):
        """Simulation of complete game - win"""
        state = init_state("cat", 5)
        
        # Guesses: c, a, t
        apply_guess(state, "c")
        self.assertEqual(state["display"], ["c", "_", "_"])
        
        apply_guess(state, "a")
        self.assertEqual(state["display"], ["c", "a", "_"])
        
        apply_guess(state, "t")
        self.assertEqual(state["display"], ["c", "a", "t"])
        
        self.assertTrue(is_won(state))
        self.assertFalse(is_lost(state))

    def test_full_game_scenario_lose(self):
        """Simulation of complete game - loss"""
        state = init_state("cat", 2)
        
        # Wrong guesses: x, y
        apply_guess(state, "x")
        apply_guess(state, "y")
        
        self.assertTrue(is_lost(state))
        self.assertFalse(is_won(state))


if __name__ == "__main__":
    unittest.main()
