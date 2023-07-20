from pprint import pprint as pretty_print
from rich.panel import Panel
from platform import system
from pathlib import Path
from .utils import funny_text
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

    def __init__(self, config_file_path: Path):
        print(funny_text)
        self.config_path = config_file_path

    def create_template_makefile_env(self, config_file_path: Path|str) -> None:
        """If the makefile env file is not found, create a template"""

        if config_file_path.exists():
            return
        else:
            try:
                config_file_path.touch()
            except Exception as e:
                print(f"Could not create template file: {str(e)}")

    def parse_makefile_env(self, file_path: Path|str) -> dict:
        variables = {} | POSSIBLE_KEYS
        print(f"Reading configuration file: {file_path}")
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
                                raise KeyError(f"Unknown variable: {var.strip()}")
        except FileNotFoundError:
            print("Could not find makefile.env file!")
        # Return dictionary whose values are not None
        return {key: value for key, value in variables.items() if value is not None}

    def read_config_file(self, makefile_env_path) -> dict:
        try:
            variables = self.parse_makefile_env(makefile_env_path)
        except Exception as e:
            raise Exception(f"Could not parse makefile.env file: {str(e)}")
        return variables

    def run(self):
        try:
            CONFIG_FILE: dict = self.read_config_file(PROJECT_DIR)
        except FileNotFoundError or Exception as e:
            CONFIG_FILE: dict = self.create_template_makefile_env()
        pretty_print(CONFIG_FILE)

if __name__ == "__main__":
    # Path for the syfala user configuration file
    PROJECT_DIR = Path.home() / 'syfala-project' / 'makefile.env'
    app = Tui(PROJECT_DIR)
    app.run()