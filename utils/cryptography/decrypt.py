import os
from cryptography.fernet import Fernet


cwd = os.getcwd()
SOURCE_FOLDER = cwd + "/" + "utils" + "/" + "cryptography"


def decrypt_file(file_path, key):
    if file_path.endswith('.encrypted'):
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)

        decrypted_file_path = file_path.replace('.encrypted', '')
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        os.remove(file_path)


def decrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.encrypted'):
                encrypted_file_path = os.path.join(root, file)
                decrypt_file(encrypted_file_path, key)


def decrypt(*args) -> None:
    try:
        key_filename = SOURCE_FOLDER + '/' + 'key.key'
        with open(key_filename, 'rb') as key_file:
            key = key_file.read()

        message_list = []
        for i in args:
            if os.path.isfile(i + '.encrypted'):
                decrypt_file(i + '.encrypted', key)
                decrypted_file_path = i
                message_list.append(decrypted_file_path + '    ' + 'FILE' + '    ' + 'DECRYPTED')
            else:
                decrypt_folder(i, key)
                decrypted_folder_path = i
                message_list.append(decrypted_folder_path + '    ' + 'FOLDER' + '    ' + 'DECRYPTED')

        return message_list

    except Exception as e:
        print(str(e))