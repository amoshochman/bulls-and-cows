import argparse
import itertools
import random
import sys
import time

my_seed = random.randrange(sys.maxsize)
random.seed(my_seed)

TIME_BETWEEN_GUESSES = 0.3  # just to get the feeling of the real time game


class Guess:
    def __init__(self, number, master):
        print("The guesser guessed: ", number)
        self.number = number
        bulls, cows = master.get_feedback(number)
        self.bulls = bulls
        self.cows = cows
        self.points = bulls + cows


class Master:

    def __init__(self, answer=None):
        self.answer = answer if answer else random.sample(range(10), 4)
        print("The master thought of: ", self.answer, end='\n-------------------------------------\n')
        self.guesses = 0

    def get_feedback(self, guess, given_answer=None):
        if given_answer:
            correct_answer = given_answer
        else:
            correct_answer = self.answer
            time.sleep(TIME_BETWEEN_GUESSES)
            self.guesses += 1
        answer_set = set(correct_answer)
        guess_set = set(guess)
        intersection = answer_set.intersection(guess_set)
        bulls = sum(a == b for a, b in zip(correct_answer, guess))
        cows = len(intersection) - bulls
        return bulls, cows


class Guesser:

    def __init__(self, master):
        self.master = master
        self.untested_digits = list(i for i in range(0, 10))

    def guess(self):
        unsorted_answer = self.get_unsorted_answer()
        return self.get_sorted_answer(unsorted_answer)

    def get_unsorted_answer(self):
        cur_guess = Guess([0, 1, 2, 3], self.master)
        i = 0
        while cur_guess.points < 4:
            next_number = cur_guess.number.copy()
            next_number[i] = self.untested_digits.pop()
            next_guess = Guess(next_number, self.master)
            if cur_guess.points != next_guess.points:
                i += 1
                if cur_guess.points < next_guess.points:
                    cur_guess = next_guess
            else:
                cur_guess, i = self.tie_break(cur_guess, next_guess, i)
        return cur_guess

    def get_sorted_answer(self, unsorted_answer):
        guess = unsorted_answer
        possible_answers = [list(elem) for elem in itertools.permutations(guess.number) if
                            self.is_potential_answer_possible(elem, guess)]
        while 1 < len(possible_answers):
            guess = Guess(possible_answers[0], self.master)
            possible_answers = [elem for elem in possible_answers if self.is_potential_answer_possible(elem, guess)]
        answer = possible_answers[0]
        print("The guesser is left with just one option so that should be the answer! ", answer)
        return answer

    def is_potential_answer_possible(self, potential_answer, bad_answer):
        potential_answer_bulls, _ = self.master.get_feedback(bad_answer.number, potential_answer)
        return potential_answer_bulls == bad_answer.bulls

    def tie_break(self, cur_guess, next_guess, i):
        digits = [cur_guess.number[i], next_guess.number[i]]
        while True:
            cur_guess = next_guess
            next_number = cur_guess.number.copy()
            next_number[i] = self.untested_digits.pop()
            next_guess = Guess(next_number, self.master)
            delta = next_guess.points - cur_guess.points
            if 0 < delta:
                return next_guess, i + 1
            if delta == 0:
                digits.append(next_guess.number[i])
                continue
            if delta < 0:
                next_number = next_guess.number
                for index, digit in enumerate(digits):
                    next_number[i + index] = digit
                    if index != 0:
                        self.untested_digits.append(digit)
                return Guess(next_number, self.master), i + len(digits)


def validate_input(n):
    if not n:
        return None
    if len(n) != 4:
        sys.exit("Error: The number should be 4 digits long!")
    if not n.isdigit():
        sys.exit("Error: The number should be digits only!")
    if len(set(n)) != 4:
        sys.exit("Error: The number should have 4 distinct digits!")
    return [int(digit) for digit in n]


def main():
    parser = argparse.ArgumentParser(
        description='Bulls and Cows game. It not passing any number, it will try to guess a random number.')
    parser.add_argument('-n', help='Optionally, the number of 4 digits to be guessed', required=False)
    args = vars(parser.parse_args())
    number = validate_input(args['n'])
    master = Master(number)
    guesser = Guesser(master)
    guesser.guess()
    print("total guesses: ", master.guesses)


if __name__ == '__main__':
    main()
