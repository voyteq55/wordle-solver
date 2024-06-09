import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QLabel, QWidget, QVBoxLayout, \
    QMessageBox, QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog

from SolutionOptimizer import SolutionOptimizer
from WordleGame import WordleGame

POSSIBLE_WORDS_LABEL = "Possible words ({}):"


class WordleSolver:
    """
    A main class responsible for connecting the user interface with the algorithmic logic
    """
    def __init__(self, words_file_path: str):
        """
        Initializes the WordleSolver with the specified list of words allowed in the current game
        :param words_file_path: path to the file which contains permitted words
        """
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

    def load_allowed_words(self, words_file_path: str) -> None:
        """
        Loads the list of allowed words from a file specified by its path into memory, raises an exception if the file
        format is invalid
        :param words_file_path: path to the file which contains permitted words
        """
        with open(words_file_path) as file:
            new_allowed_words = []
            for word in file.readlines():
                if len(word.strip()) != 5:
                    raise ValueError("File must contain only 5-letter words on each line")
                new_allowed_words.append(word.strip())
            self.allowed_words = new_allowed_words

    def update_game(self) -> None:
        """
        Updates the state to its next row, if the entered word is valid and allowed (included in the recognized words)
        """
        self.current_game.setFocus()
        if entered_word := self.current_game.get_word_if_valid():
            if entered_word in self.allowed_words:
                word_result = self.current_game.get_word_result()
                self.solution_optimizer.eliminate_words(user_guess=entered_word, result_combination=word_result)
                self.update_word_suggestions()
                self.current_game.move_to_next_word()
            else:
                QMessageBox.information(self.current_game, "Incorrect word", f"The word {entered_word} was not found")

    def update_word_suggestions(self) -> None:
        """
        Updates the widget list of possible and best words based on the current state of the game
        """
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

    def reset(self) -> None:
        """
        Resets the gameplay to its initial stage so that the user can start again
        """
        self.current_game.reset()
        self.solution_optimizer.set_possible_words()
        self.update_word_suggestions()

    def import_words_from_file(self) -> None:
        """
        Prompts a user to pick a file with words to import, if the choice fails it shows an appropriate message box
        """
        try:
            file_dialog = QFileDialog(self.window)
            file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
            file_dialog.setViewMode(QFileDialog.Detail)
            file_path, _ = file_dialog.getOpenFileName(self.window, "Select File", "",
                                                       "Text Files (*.txt);;All Files (*)")
            self.load_allowed_words(file_path)
            self.current_game.set_allowed_letters(self.allowed_words)
            self.solution_optimizer.set_allowed_words(self.allowed_words)
            self.reset()
        except FileNotFoundError:
            QMessageBox.information(self.current_game, "File Not Found", "No valid file was selected")
        except ValueError:
            QMessageBox.information(self.current_game, "Invalid file format",
                                    "File format is invalid (it should only contain 5-letter words on each line")

    def setup_ui(self) -> None:
        """
        Sets up graphical user interface widgets and their layout, must be executed after initializing WordleSolver
        """
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
