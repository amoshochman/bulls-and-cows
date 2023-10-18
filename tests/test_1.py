import sys
import os

import pytest

tests_folder = os.path.dirname(os.path.realpath(__file__))
parent_folder = os.path.join(tests_folder, '..')
sys.path.append(parent_folder)
import bulls_and_cows


@pytest.fixture
def mock_sleep():
    bulls_and_cows.TIME_BETWEEN_GUESSES = 0


def test_1(mock_sleep):
    iterations = 100
    for _ in range(iterations):
        game = bulls_and_cows.Master()
        guesser = bulls_and_cows.Guesser(game)
        final_guess = guesser.guess()
        assert list(final_guess) == game.answer
