from PySide6.QtWidgets import QLabel

LETTER_BOX_STYLE = "background-color: {}; color: black; font-size: 24px; qproperty-alignment: 'AlignCenter';"
WHITE = "#eee"


class LetterBox(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("")
        self.setFixedSize(50, 50)
        self.setStyleSheet(LETTER_BOX_STYLE.format(WHITE))
