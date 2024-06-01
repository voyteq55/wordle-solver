from PySide6.QtWidgets import QLabel

LETTER_BOX_STYLE = "background-color: {}; color: black; font-size: 24px; qproperty-alignment: 'AlignCenter';"
WHITE = "#eee"
YELLOW = "#f3c237"
GREEN = "#79b851"


class LetterBox(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("")
        self.setFixedSize(50, 50)
        self.state = "-"
        self.setStyleSheet(LETTER_BOX_STYLE.format(WHITE))

    def mousePressEvent(self, event):
        self.change_state()

    def change_state(self):
        if self.state == "-":
            self.state = "^"
            self.setStyleSheet(LETTER_BOX_STYLE.format(YELLOW))
        elif self.state == "^":
            self.state = "*"
            self.setStyleSheet(LETTER_BOX_STYLE.format(GREEN))
        elif self.state == "*":
            self.state = "-"
            self.setStyleSheet(LETTER_BOX_STYLE.format(WHITE))