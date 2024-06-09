from PySide6.QtWidgets import QLabel

import LetterPlacement

LETTER_BOX_STYLE = "background-color: {}; color: black; font-size: 24px; qproperty-alignment: 'AlignCenter';"
WHITE = "#eee"
YELLOW = "#f3c237"
GREEN = "#79b851"


class LetterBox(QLabel):
    """
    A class representing one box in a 5x5 grid, containing at most one letter
    """
    def __init__(self):
        """
        Initializes the LetterBox
        """
        super().__init__()
        self.state = None
        self.initialize()

    def initialize(self) -> None:
        """
        Sets the initial style parameters of a box
        """
        self.setText("")
        self.setFixedSize(50, 50)
        self.state = LetterPlacement.WRONG
        self.setStyleSheet(LETTER_BOX_STYLE.format(WHITE))

    def mousePressEvent(self, event) -> None:
        self.change_state()

    def change_state(self) -> None:
        """
        Changes between the wrong, misplaced, and correct placements of a letter
        """
        if self.state == LetterPlacement.WRONG:
            self.state = LetterPlacement.MISPLACED
            self.setStyleSheet(LETTER_BOX_STYLE.format(YELLOW))
        elif self.state == LetterPlacement.MISPLACED:
            self.state = LetterPlacement.CORRECT
            self.setStyleSheet(LETTER_BOX_STYLE.format(GREEN))
        elif self.state == LetterPlacement.CORRECT:
            self.state = LetterPlacement.WRONG
            self.setStyleSheet(LETTER_BOX_STYLE.format(WHITE))
