import os
from cryptography.fernet import Fernet


cwd = os.getcwd()
SOURCE_FOLDER = cwd + "/" + "utils" + "/" + "cryptography"


def generate_key():
    return Fernet.generate_key()


def save_key_to_file(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)


def load_key_from_file(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key


def encrypt_file(file_path, key):
    if not file_path.endswith('.encrypted'):
        with open(file_path, 'rb') as file:
            data = file.read()

        f = Fernet(key)
        encrypted_data = f.encrypt(data)

        with open(file_path + '.encrypted', 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        os.remove(file_path)


def encrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)


def encrypt(*args) -> None:
    try:
        key = ''
        if not 'key.key' in os.listdir(SOURCE_FOLDER):
            key = generate_key()

            key_filename = SOURCE_FOLDER + '/' + 'key.key'
            save_key_to_file(key, key_filename)
        else:
            with open(SOURCE_FOLDER + "/" +'key.key', 'rb') as key_file:
                key = key_file.read()

        message_list = []
        for i in args:
            if os.path.isfile(i):
                encrypt_file(i, key)

                encrypted_file_path = i + '.encrypted' + '    ' + 'FILE' + '    ' + 'ENCRYPTED'
                message_list.append(encrypted_file_path)
            else:
                encrypt_folder(i, key)
                encrypted_file_path = i + '    ' + 'FOLDER' + '    ' + 'ENCRYPTED'
                message_list.append(encrypted_file_path)

        return message_list

    except Exception as e:
        print(str(e))
