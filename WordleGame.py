from typing import List

from PySide6.QtWidgets import QWidget

from LetterBox import LetterBox


class WordleGame(QWidget):
    def __init__(self, allowed_words):
        super().__init__()
        self.allowed_letters = set(letter for word in allowed_words for letter in word)
        self.current_column = 0
        self.current_row = 0
        self.letter_boxes: List[List[LetterBox]] = []
        for i in range(6):
            row = []
            for j in range(5):
                row.append(LetterBox())
            self.letter_boxes.append(row)
        self.update_boxes_clickability()

    def reset(self):
        self.current_column = 0
        self.current_row = 0
        for row in self.letter_boxes:
            for box in row:
                box.initialize()
        self.update_boxes_clickability()

    def move_to_next_word(self):
        self.current_row += 1
        self.current_column = 0
        self.update_boxes_clickability()

    def update_boxes_clickability(self):
        for row_i in range(6):
            is_row_enabled = row_i == self.current_row
            for box in self.letter_boxes[row_i]:
                box.setEnabled(is_row_enabled)

    def get_word_if_valid(self) -> str | None:
        word = "".join(self.letter_boxes[self.current_row][i].text() for i in range(5))
        if len(word) == 5 and all(letter in self.allowed_letters for letter in word):
            return word

    def get_word_result(self) -> str:
        return "".join(self.letter_boxes[self.current_row][i].state for i in range(5))

    def keyPressEvent(self, event):
        letter = str.lower(event.text())
        if letter == chr(8) or letter == chr(127):  # backspace
            if self.current_column > 0:
                self.current_column -= 1
                self.letter_boxes[self.current_row][self.current_column].setText("")
        elif self.current_column < 5 and self.current_row < 6 and letter in self.allowed_letters:
            self.letter_boxes[self.current_row][self.current_column].setText(letter)
            self.current_column += 1
