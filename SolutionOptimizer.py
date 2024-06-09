import math
from typing import List, Tuple

from CombinationSolver import CombinationSolver


class SolutionOptimizer:
    """
    A class responsible for the main algorithm, calculating the entropy of each allowed word and narrowing down
    the list of possible solutions
    """
    def __init__(self, allowed_words: List[str]):
        """
        Initializes the SolutionOptimizer
        :param allowed_words: List of words permitted in the current game
        """
        self.allowed_words = allowed_words
        self.possible_words_left = None
        self.combination_solver = CombinationSolver(allowed_words)
        self.set_possible_words()

    def set_possible_words(self) -> None:
        """
        Resets the list representing possible solutions to be the same as all the allowed words
        """
        self.possible_words_left = list(self.allowed_words)

    def set_allowed_words(self, allowed_words: List[str]) -> None:
        """
        Assigns the allowed words and adjusts the combination solver for the new list of words
        :param allowed_words: List of words permitted in the current game
        """
        self.allowed_words = allowed_words
        self.combination_solver.combination_dict = {}
        self.combination_solver.setup_combination_dictionary(self.allowed_words)

    def eliminate_words(self, user_guess: str, result_combination: str) -> None:
        """
        Removes the words which are no longer considered as possible solutions based on the new result of a guess
        :param user_guess: Word entered as a guess
        :param result_combination: Resulting 5-character string representing letter placements of the guessed word
        """
        self.possible_words_left = [word for word in self.possible_words_left if
                                    self.combination_solver.get_result(user_guess, word) == result_combination]

    def calculate_entropy_bits(self) -> List[Tuple[str, float]]:
        """
        For every allowed words calculates its corresponding bits of entropy, i.e. how much this word is expected to
        narrow down the list of possible solutions
        :return: List of tuples, each having 2 items:
                    The first: Word, potential guess
                    The second: Float number representing number of bits of entropy which this word is expected to
                                generate (on average), which is a measure of how much information a given word is
                                expected to provide
        """
        if len(self.possible_words_left) <= 1:
            return []
        entropy_bits = []
        for allowed_user_guess in self.allowed_words:
            combination_count = {}
            for possible_word in self.possible_words_left:
                combination = self.combination_solver.get_result(allowed_user_guess, possible_word)
                if combination not in combination_count:
                    combination_count[combination] = 0
                combination_count[combination] += 1

            combination_probability = {}
            for combination in combination_count:
                combination_probability[combination] = combination_count[combination] / len(self.possible_words_left)
            bits_of_entropy = 0
            for combination in combination_probability:
                p = combination_probability[combination]
                bits_of_entropy += p * math.log2(1 / p)

            entropy_bits.append((allowed_user_guess, bits_of_entropy))

        entropy_bits.sort(key=lambda entry: (entry[1], entry[0] in self.possible_words_left), reverse=True)
        return entropy_bits
