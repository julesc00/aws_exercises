import os
import sys

current_script_path = os.path.abspath(__file__)
folder_name = "src"
project_directory_path = current_script_path.split(folder_name)[0] + folder_name
sys.path.append(project_directory_path)
