from typing import List

from PySide6.QtWidgets import QWidget

from LetterBox import LetterBox


class WordleGame(QWidget):
    """
    A class representing the current state of the gameplay, attempted words and their results
    """
    def __init__(self, allowed_words: List[str]):
        """
        Initializes the WordleGame
        :param allowed_words: List of words permitted in the current game
        """
        super().__init__()
        self.allowed_letters = None
        self.set_allowed_letters(allowed_words)
        self.current_column = 0
        self.current_row = 0
        self.letter_boxes: List[List[LetterBox]] = []
        for i in range(6):
            row = []
            for j in range(5):
                row.append(LetterBox())
            self.letter_boxes.append(row)
        self.update_boxes_clickability()

    def set_allowed_letters(self, allowed_words: List[str]) -> None:
        """
        Extracts all letters which occur in the allowed words and saves them in a set for quick retrieval
        :param allowed_words: List of words permitted in the current game
        """
        self.allowed_letters = set(letter for word in allowed_words for letter in word)

    def reset(self) -> None:
        """
        Resets the state of the game to its initial stage
        """
        self.current_column = 0
        self.current_row = 0
        for row in self.letter_boxes:
            for box in row:
                box.initialize()
        self.update_boxes_clickability()

    def move_to_next_word(self) -> None:
        """
        Moves the focus to the beginning of the next row, so that the user can enter the next word
        """
        self.current_row += 1
        self.current_column = 0
        self.update_boxes_clickability()

    def update_boxes_clickability(self) -> None:
        """
        Sets the boxes in the current row as modifiable in the context of their state, while the rest are not enabled
        """
        for row_i in range(6):
            is_row_enabled = row_i == self.current_row
            for box in self.letter_boxes[row_i]:
                box.setEnabled(is_row_enabled)

    def get_word_if_valid(self) -> str | None:
        """
        Returns the word from the current row if it's fully entered, otherwise returns None
        :return: Word entered through the interface by the user or None
        """
        word = "".join(self.letter_boxes[self.current_row][i].text() for i in range(5))
        if len(word) == 5 and all(letter in self.allowed_letters for letter in word):
            return word

    def get_word_result(self) -> str:
        """
        Returns the result of the guess entered by the user in the current row
        :return: Result of the guess
        """
        return "".join(self.letter_boxes[self.current_row][i].state for i in range(5))

    def keyPressEvent(self, event):
        """
        Handles keyboard input, adds entered letter to the boxes if possible, removes after pressing backspace
        :param event: QKeyEvent containing information about which key was pressed
        """
        letter = str.lower(event.text())
        if letter == chr(8) or letter == chr(127):  # backspace
            if self.current_column > 0:
                self.current_column -= 1
                self.letter_boxes[self.current_row][self.current_column].setText("")
        elif self.current_column < 5 and self.current_row < 6 and letter in self.allowed_letters:
            self.letter_boxes[self.current_row][self.current_column].setText(letter)
            self.current_column += 1
