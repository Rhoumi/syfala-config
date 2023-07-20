import inquirer
from rich.panel import Panel
from pathlib import Path
import json

FUNNY_TEXT = """
███████╗██╗   ██╗███████╗ █████╗ ██╗      █████╗ 
██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗██║     ██╔══██╗
███████╗ ╚████╔╝ █████╗  ███████║██║     ███████║
╚════██║  ╚██╔╝  ██╔══╝  ██╔══██║██║     ██╔══██║
███████║   ██║   ██║     ██║  ██║███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
This is the configuration tool for Syfala.
"""

# Appdirs boilerplate code
APP_NAME, APP_AUTHOR = "Syfala", "Emeraude"
USER_DIR = '$HOME/syfala-project'
makefile_env_file = USER_DIR + '/makefile.env'
json_output_file = 'config.json'


def parse_makefile_env(file_path):
    variables = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#') and ':=' in line:
                var, value = line.split(':=')
                variables[var.strip()] = value.strip()
    return variables

def convert_to_json(makefile_env_path, json_path):
    try:
        variables = parse_makefile_env(makefile_env_path)
        with open(json_path, 'w') as json_file:
            json.dump(variables, json_file, indent=4)
        print('Conversion successful!')
    except FileNotFoundError:
        print(f"File not found: {makefile_env_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


convert_to_json(makefile_env_file, json_output_file)

def read_json_file():
    with open(str(json_output_file), "r") as jsonFile:
        return json.load(jsonFile)


def write_json_file(data: dict):
    with open(str(json_output_file), "w") as jsonFile:
        json.dump(data, jsonFile, indent=4, sort_keys=True)








def main():

    MENU= [
        "Variables",
        "Build_Targets"
    ]

    Variables_Xilinx = [
        "XILINX_ROOT_DIR",
        "XILINX_VERSION"    
        ]

    Variables_Target = [
        "TARGET"
        ]

    Variables_Target_Faust = [
        "FAUST",
        "FAUST_MCD",
        "FAUST_DSP_TARGET",
        "FAUST_HLS_ARCH_FILE",
        "FAUST_ARM_ARCH_FILE",
        ]

    Variables_Target_cpp = [
        "HLS_CPP_SOURCE",
        "HOST_MAIN_SOURCE",
        "INPUTS",
        "OUTPUTS",
        ]
    
    Variables_Board = [
        "BOARD",
        "BOARD_CONSTRAINT_FILE",
        ]

    Variables_Runtime = [
        "SAMPLE_RATE",
        "SAMPLE_WIDTH",
        "MULTISAMPLE",
        "MEMORY_TARGET",
        "CONTROLLER_TYPE",
        "CTRL_MIDI",
        "CTRL_OSC",
        "CTRL_HTTP",
        ]

    Variables_Advanced = [
        "LINUX",
        "CONFIG_EXPERIMENTAL_TDM",
        "CONFIG_EXPERIMENTAL_SIGMA_DELTA",
        "PREPROCESSOR_HLS",
        "PREPROCESSOR_I2S",
        "I2S_SOURCE",
        "BD_TARGET",
        ]

    Build_Targets = [
        "all",
        "sw",
        "hw",
        "bitstream",
        "synth",
        "project",
        "hls",
        "hls-target-file",
        ]

    Build_linux = [
        "linux",
        "linux-boot",
        "linux-root",
        ]




# Définition des questions pour chaque onglet
tab1_questions = [
    inquirer.Checkbox('fruits', message="Quels fruits aimez-vous ?", 
        choices=['Pomme', 'Banane', 'Orange', 'Mangue'])
]

tab2_questions = [
    inquirer.Checkbox('animaux', message="Quels animaux préférez-vous ?", choices=['Chien', 'Chat', 'Oiseau', 'Lion'])
]

tabs = [
    {
        'name': 'tab1',
        'questions': tab1_questions,
    },
    {
        'name': 'tab2',
        'questions': tab2_questions,
    }
]

# Fonction pour sélectionner un onglet
def select_tab(answers):
    return answers['tab']

# Création du formulaire d'onglets
questions = [
    inquirer.List('tab', message="Sélectionnez un onglet :", choices=['tab1', 'tab2'])
]

answers = inquirer.prompt(questions)
selected_tab = select_tab(answers)

# Affichage des questions de l'onglet sélectionné
selected_tab_questions = next(item for item in tabs if item['name'] == selected_tab)['questions']
tab_answers = inquirer.prompt(selected_tab_questions)

# Affichage des réponses
print("Vos réponses :")
for key, value in tab_answers.items():
    print(f"{key}: {value}")


