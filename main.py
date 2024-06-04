from WordleSolver import WordleSolver

DEFAULT_WORDS_FILE_PATH = "words/polish_words.txt"


def main():
    solver = WordleSolver(DEFAULT_WORDS_FILE_PATH)
    solver.setup_ui()


if __name__ == '__main__':
    main()
