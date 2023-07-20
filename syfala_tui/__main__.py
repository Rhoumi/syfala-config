from pprint import pprint as pretty_print
from rich.panel import Panel
from typing import Optional
from platform import system
from .utils import _banner 
from pathlib import Path
import inquirer

POSSIBLE_KEYS = {
    # XILINX RELATED OPTIONS
    "XILINX_ROOT_DIR": None,
    "XILINX_VERSION": None,    
    # TARGET
    "TARGET": None,
    # TARGET FAUST
    "FAUST": None,
    "FAUST_MCD": None,
    "FAUST_DSP_TARGET": None,
    "FAUST_HLS_ARCH_FILE": None,
    "FAUST_ARM_ARCH_FILE": None,
    # TARGET CPP
    "HLS_CPP_SOURCE": None,
    "HOST_MAIN_SOURCE": None,
    "INPUTS": None,
    "OUTPUTS": None,
    # BOARD TARGET
    "BOARD": None,
    "BOARD_CONSTRAINT_FILE": None,
    # RUNTIME PARAMETERS
    "SAMPLE_RATE": None,
    "SAMPLE_WIDTH": None,
    "MULTISAMPLE": None,
    "MEMORY_TARGET": None,
    "CONTROLLER_TYPE": None,
    "CTRL_MIDI": None,
    "CTRL_OSC": None,
    "CTRL_HTTP": None,
    # ADVANCED BUILD OPTIONS
    "LINUX": None,
    "CONFIG_EXPERIMENTAL_TDM": None,
    "CONFIG_EXPERIMENTAL_SIGMA_DELTA": None,
    "PREPROCESSOR_HLS": None,
    "PREPROCESSOR_I2S": None,
    "I2S_SOURCE": None,
    "BD_TARGET": None,
    # HW/SW BUILD OPTIONS
    "all": None,
    "sw": None,
    "hw": None,
    "bitstream": None,
    "synth": None,
    "project": None,
    "hls": None,
    "hls-target-file": None,
    "linux": None,
    "linux-boot": None,
    "linux-root": None,
}


# Find the project directory located in the home directory + syfala-project

class Tui:

    def __init__(self, config: Path):
        print(_banner)
        self.config_path = config
        self.config_file: Optional[dict] = None
        try:
            self.config_file: dict = self._read_config_file(self.config_path)
        except FileNotFoundError or Exception as e:
            self.config_file: dict = self._create_template_makefile_env()


    def _create_template_makefile_env(self, config_file_path: Path|str) -> None:
        """If the makefile.env file does not exist, create a template file.
        The template file will be created in the default syfala-project 
        directory. If the directory does not exist, it will be created.

        Args:
            config_file_path (Path | str): Path to the makefile.env file
        """
        if config_file_path.exists() and config_file_path.is_file():
            return
        else:
            print('====> Creating makefile.env file (and possibly syfala-project directory)')
            try:
                if not config_file_path.parent.exists():
                    config_file_path.parent.mkdir(parents=True)
                    config_file_path.touch()
                else:
                    config_file_path.touch()
            except Exception as e:
                raise Exception(f"Could not create makefile.env file: {str(e)}")
        return self._parse_makefile_env(config_file_path)

    def _parse_makefile_env(self, file_path: Path|str) -> dict:
        """Parse the makefile.env file and return a dictionary with the
        variables and their values. If the file does not exist, return
        an empty dictionary.

        Args:
            file_path (Path | str): Path to the makefile.env file

        Returns:
            dict: Dictionary containing the config variables and their values
        """
        variables = {} | POSSIBLE_KEYS
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if not line.startswith('#') and ':=' in line:
                            var, value = line.split(':=')
                            if var.strip() in POSSIBLE_KEYS.keys():
                                variables[var.strip()] = value.strip()
                            else:
                                print(f'====> Unknown variable in config file: {var.strip()}')
        except FileNotFoundError:
            variables = self._create_template_makefile_env(file_path)

        # Return dictionary whose values are not None
        return {key: value for key, value in variables.items() if value is not None}

    def _read_config_file(self, makefile_env_path) -> dict:
        """Entry point for reading the makefile.env file. This function
        will try to parse the makefile.env file and return a dictionary

        Args:
            makefile_env_path (_type_): Path to the makefile.env file

        Raises:
            Exception: Exception raised if the makefile.env file 
            could not be parsed. Note that the program will try
            to create a template makefile.env file if it does not
            exist or is invalid.

        Returns:
            dict: Dictionary containing the syfala config variables and their values 
        """
        return self._parse_makefile_env(makefile_env_path)

    def _variables_menu(self, config_file: dict) -> dict:
        ...
    
    def _build_targets_menu(self, config_file: dict) -> dict:
        ...

    def _write_config_file(self, config_file: dict) -> None:
        ...

    def _main_menu(self):
        answer = inquirer.prompt([
            inquirer.List(
                "choice",
                message="Do you want to modify variables or build targets?",
                choices=["Variables", "Build Targets", "Exit"],
            ),
        ])
        if answer.get('choice') == 'Variables':
            self.config_file = self._variables_menu(self.config_file)
        elif answer.get('choice') == 'Build Targets':
            self.config_file = self._build_targets_menu(self.config_file)
        else:
            print('====> Writing config file!')
            self._write_config_file(self.config_file)
            exit(0)

    def run(self):
        self._main_menu()


if __name__ == "__main__":
    # Path for the syfala user configuration file
    PROJECT_DIR = Path.home() / 'syfala-project' / 'makefile.env'
    app = Tui(PROJECT_DIR)
    app.run()