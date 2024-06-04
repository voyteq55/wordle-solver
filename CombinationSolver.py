from typing import List, Dict


class CombinationSolver:
    def __init__(self, allowed_words: List[str]):
        self.combination_dict: Dict[str, Dict[str, str]] = {}
        self.setup_combination_dictionary(allowed_words)

    def setup_combination_dictionary(self, allowed_words: list) -> None:
        for user_guess in allowed_words:
            self.combination_dict[user_guess] = {}

        for word_to_guess in allowed_words:
            for user_guess in allowed_words:
                result = ["", "", "", "", ""]
                letters_to_guess = [ltr for ltr in word_to_guess]
                indexes_with_correct_letters = []
                for letter_index in range(5):
                    if user_guess[letter_index] == letters_to_guess[letter_index]:
                        result[letter_index] = "*"
                        letters_to_guess[letter_index] = ""
                        indexes_with_correct_letters.append(letter_index)
                for letter_index in range(5):
                    if letter_index not in indexes_with_correct_letters:
                        if user_guess[letter_index] in letters_to_guess:
                            result[letter_index] = "^"
                            letters_to_guess[letters_to_guess.index(user_guess[letter_index])] = ""
                        else:
                            result[letter_index] = "-"
                self.combination_dict[user_guess][word_to_guess] = "".join(result)

    def get_result(self, user_guess: str, word_to_guess: str) -> str:
        return self.combination_dict[user_guess][word_to_guess]
