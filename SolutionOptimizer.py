import math
from typing import List, Tuple

from CombinationSolver import CombinationSolver


class SolutionOptimizer:
    def __init__(self, allowed_words: List[str]):
        self.allowed_words = allowed_words
        self.possible_words_left = list(self.allowed_words)
        self.combination_solver = CombinationSolver(allowed_words)

    def eliminate_words(self, user_guess: str, result_combination: str) -> None:
        self.possible_words_left = [word for word in self.possible_words_left if
                                    self.combination_solver.get_result(user_guess, word) == result_combination]

    def calculate_entropy_bits(self) -> List[Tuple[str, float]]:
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
