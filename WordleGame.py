from typing import List

from PySide6.QtWidgets import QWidget

from LetterBox import LetterBox


class WordleGame(QWidget):
    def __init__(self):
        super().__init__()
        self.current_column = 0
        self.current_row = 0
        self.letter_boxes: List[List[LetterBox]] = []
        for i in range(6):
            row = []
            for j in range(5):
                row.append(LetterBox())
            self.letter_boxes.append(row)

    def keyPressEvent(self, event):
        letter = str.lower(event.text())
        if letter == chr(8) or letter == chr(127):  # backspace
            if self.current_column > 0:
                self.current_column -= 1
                self.letter_boxes[self.current_row][self.current_column].setText("")
        elif self.current_column < 5:
            self.letter_boxes[self.current_row][self.current_column].setText(letter)
            self.current_column += 1

