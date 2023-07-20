import inquirer

FILE_PATH = "makefile.env"
VARIABLE_LIST = ["", ""]


class SyfalaConfig:
    def __init__(self):

        # 1: reading and validating variable file
        try:
            self.variables = self.read_variables_file(FILE_PATH)
        except RuntimeError:
            print("Cannot read makefile.env file.")
            exit()

    def read_variables_file(self):
        ...

    def prompt(self):
        ...


if __name__ == "__main__":
    tui = SyfalaConfig()
    answers = tui.prompt()
    # Then, process into definitive file
    # ...
