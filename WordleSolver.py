import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QLabel, QWidget, QVBoxLayout, \
    QMessageBox, QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog

from SolutionOptimizer import SolutionOptimizer
from WordleGame import WordleGame

POSSIBLE_WORDS_LABEL = "Possible words ({}):"


class WordleSolver:
    def __init__(self, words_file_path: str):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.allowed_words = []
        self.load_allowed_words(words_file_path)
        self.current_game = WordleGame(self.allowed_words)
        self.possible_words_label = QLabel()
        self.possible_words_widget = QListWidget()
        self.best_words_widget = QListWidget()
        self.letter_boxes_layout = QGridLayout()
        self.solution_optimizer = SolutionOptimizer(self.allowed_words)
        self.update_word_suggestions()

    def load_allowed_words(self, words_file_path: str):
        with open(words_file_path) as file:
            self.allowed_words = list(word.strip() for word in file.readlines())

    def update_game(self):
        self.current_game.setFocus()
        if entered_word := self.current_game.get_word_if_valid():
            if entered_word in self.allowed_words:
                word_result = self.current_game.get_word_result()
                self.solution_optimizer.eliminate_words(user_guess=entered_word, result_combination=word_result)
                self.update_word_suggestions()
                self.current_game.move_to_next_word()
            else:
                QMessageBox.information(self.current_game, "Incorrect word", f"The word {entered_word} was not found")

    def update_word_suggestions(self):
        entropies = self.solution_optimizer.calculate_entropy_bits()
        self.best_words_widget.clear()
        for allowed_user_guess, entropy_bits in entropies:
            item = QListWidgetItem(f"{allowed_user_guess}: {entropy_bits:.3f}")
            self.best_words_widget.addItem(item)
        self.possible_words_widget.clear()
        sorted_possible_words = sorted(self.solution_optimizer.possible_words_left)
        self.possible_words_label.setText(POSSIBLE_WORDS_LABEL.format(len(sorted_possible_words)))
        for possible_word in sorted_possible_words:
            item = QListWidgetItem(possible_word)
            self.possible_words_widget.addItem(item)

    def reset(self):
        self.current_game.reset()
        self.solution_optimizer.set_possible_words()
        self.update_word_suggestions()

    def import_words_from_file(self):
        try:
            file_dialog = QFileDialog(self.window)
            file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
            file_dialog.setViewMode(QFileDialog.Detail)
            file_path, _ = file_dialog.getOpenFileName(self.window, "Select File", "", "Text Files (*.txt);;All Files "
                                                                                       "(*)")

            self.load_allowed_words(file_path)
            self.current_game.set_allowed_letters(self.allowed_words)
            self.solution_optimizer.set_allowed_words(self.allowed_words)
            self.reset()
        except FileNotFoundError:
            QMessageBox.information(self.current_game, "File Not Found", f"No valid file was selected")

    def setup_ui(self):
        self.window.setWindowTitle("Wordle Solver")

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)

        left_pane_layout = QVBoxLayout()
        left_pane_layout.addWidget(self.possible_words_label)
        left_pane_layout.addWidget(self.possible_words_widget)
        left_pane_layout.addWidget(reset_button)

        left_pane = QWidget()
        left_pane.setLayout(left_pane_layout)

        # setting up 5x6 gameplay grid
        for i in range(6):
            for j in range(5):
                self.letter_boxes_layout.addWidget(self.current_game.letter_boxes[i][j], i, j)

        letter_boxes = self.current_game
        letter_boxes.setLayout(self.letter_boxes_layout)

        next_word_button = QPushButton("Next Word")
        next_word_button.clicked.connect(self.update_game)

        middle_pane_layout = QVBoxLayout()
        middle_pane_layout.addWidget(letter_boxes)
        middle_pane_layout.addWidget(next_word_button)

        middle_pane = QWidget()
        middle_pane.setLayout(middle_pane_layout)

        import_words_button = QPushButton("Import words from a file")
        import_words_button.clicked.connect(self.import_words_from_file)

        right_pane_layout = QVBoxLayout()
        right_pane_layout.addWidget(QLabel("Best words"))
        right_pane_layout.addWidget(self.best_words_widget)
        right_pane_layout.addWidget(import_words_button)

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

        letter_boxes.setFocus()

        sys.exit(self.app.exec())
