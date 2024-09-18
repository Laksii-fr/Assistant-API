import os
import re


def get_filename_and_extension(file: str):
        # Split the filename into base and extension
        filename, file_extension = os.path.splitext(file)
        return filename, file_extension


def get_file_name(file_path):
        file_path_components = file_path.split('/')
        file_name_and_extension = file_path_components[-1].rsplit('.', 1)
        return file_name_and_extension[0]


def create_directory_structure():
        input_local_directory = '/tmp/chat-docs/inputs/'
        output_local_directory = '/tmp/chat-docs/outputs/'
        sidecar_local_directory = '/tmp/chat-docs/outputs/'
        # Create the local directory if it doesn't exist
        os.makedirs(input_local_directory, exist_ok=True)
        os.makedirs(output_local_directory, exist_ok=True)
        os.makedirs(sidecar_local_directory, exist_ok=True)
        return input_local_directory, output_local_directory, sidecar_local_directory


def replace_hyphens_with_underscores(input_string):
        # Use regular expression to replace all occurrences of '-'
        converted_string = re.sub(r'-', '_', input_string)
        # Add the 's_' prefix to the converted string
        result_string = 's_' + converted_string
        return result_string


def replace_hyphens_with_underscores_only(input_string):
        # Use regular expression to replace all occurrences of '-'
        converted_string = re.sub(r'-', '_', input_string)
        # Add the 's_' prefix to the converted string
        result_string = converted_string
        return result_string
