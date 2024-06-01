import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QVBoxLayout, \
    QHBoxLayout, QListWidget

from WordleGame import WordleGame

POSSIBLE_WORDS_LABEL = "Possible words ({}):"


class WordleSolver:
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.current_game = WordleGame()

    def setup_ui(self):
        self.window.setWindowTitle("Wordle Solver")

        left_pane_layout = QVBoxLayout()
        left_pane_layout.addWidget(QLabel("Possible words:"))
        left_pane_layout.addWidget(QListWidget())

        left_pane = QWidget()
        left_pane.setLayout(left_pane_layout)

        # setting up 5x6 gameplay grid
        letter_boxes_layout = QGridLayout()
        for i in range(6):
            for j in range(5):
                letter_boxes_layout.addWidget(self.current_game.letter_boxes[i][j], i, j)

        letter_boxes = self.current_game
        letter_boxes.setLayout(letter_boxes_layout)

        middle_pane_layout = QVBoxLayout()
        middle_pane_layout.addWidget(letter_boxes)

        middle_pane = QWidget()
        middle_pane.setLayout(middle_pane_layout)

        right_pane_layout = QVBoxLayout()
        right_pane_layout.addWidget(QLabel("Best words"))
        right_pane_layout.addWidget(QListWidget())

        right_pane = QWidget()
        right_pane.setLayout(right_pane_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_pane)
        main_layout.addWidget(middle_pane)
        main_layout.addWidget(right_pane)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.window.setCentralWidget(main_widget)
        self.window.show()

        sys.exit(self.app.exec())
