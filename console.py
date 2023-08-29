from account_management.controller import account_controller

def init():
    if __name__ == '__main__':
        try:
            token = input("token>>>\t")
            password = input("password>>>\t")
            folder_list = []
            count = 1
            while True:
                folder = input(f"full path to folder{str(count)}>>>(c to confirm)\t")
                if folder.lower() == 'c':
                    break
                count = count + 1
                folder_list.append(folder)

            # print(hash(password.encode('utf-8')))
            # print(token, password, folder_list)

            # db = dbrepository(token, password, folder_list)
            # db.create_account()
            # token = str(input('token: '))
            # res = dbrepository.get_account_by_token(token=token)
            # print(encrypt(r'./test_data'))
            # print(decrypt('./test_data'))
            account = account_controller(token, password, folder_list)
            account.create()
            print(account.read())
            update_folder_list = []
            count = 1
            while True:
                folder = input(f"full path to folder{str(count)}>>>(c to confirm)\t")
                if folder.lower() == 'c':
                    break
                count = count + 1
                update_folder_list.append(folder)
            account.add_account(token, password, update_folder_list)
            print(account.read())
            # print(account.read())
        except Exception as e:
            print('ERROR: ' + str(e))