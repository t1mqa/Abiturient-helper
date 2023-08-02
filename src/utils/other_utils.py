import re
import os


def snils_normalize(snils_string):
    snils_digits = re.sub(r'\D', '', snils_string)
    return snils_digits


def list_directories_inside_proj(relative_path):
    current_file_path = os.path.abspath(__file__)
    desired_directory = os.path.abspath(os.path.join(current_file_path, f'../../../{relative_path}'))
    if not os.path.exists(desired_directory):
        print(f"Directory not found: {desired_directory}")
        return []
    items = os.listdir(desired_directory)
    directories = [item for item in items if os.path.isdir(os.path.join(desired_directory, item))]
    return directories


def get_project_abspath():
    current_file_path = os.path.abspath(__file__)
    desired_directory = os.path.abspath(os.path.join(current_file_path, f'../../../'))
    return desired_directory


def get_data_from_file(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    globals_dict = {}
    exec(file_contents, globals_dict)
    data = globals_dict.get('SPECS')
    return data


def configure_user_positions_message(data) -> str:
    message = "Ваши места на данный момент:\n"
    for uni in data:
        message += f"\n{uni}\n(0 - участвует в конкурсе по другому приоритету)"
        for spec in data[uni]:
            arr = data[uni][spec]
            message += (f"\n\n{spec}:\nПриоритет: {arr[1]}\n"
                        f"Позиция в списке ВУЗА: {arr[3]}\n")
    return message
