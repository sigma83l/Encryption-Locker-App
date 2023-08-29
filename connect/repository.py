import sqlite3
import json
from decorators.method_tracking import track
from utils.hashing import hash, verify
from utils.cryptography.encrypt import encrypt
from utils.cryptography.decrypt import decrypt

class dbrepository:
    def __init__(self):
        pass

    # @track
    # @safe_use
    @classmethod
    def create_account(cls, token: str, pwhash: str, folder_list: str) -> None:
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS accounts 
        (id INTEGER PRIMARY KEY, token TEXT, password_hash TEXT, folder_path_list TEXT)""")
        c.execute("""SELECT token FROM accounts""")
        tokens = c.fetchall()
        # print(tokens)
        for i in tokens:
            if token == i[0]:
                raise Exception("TOKEN ALREADY EXISTS")
            else:
                continue
        c.execute(rf"""INSERT INTO accounts (token, password_hash, folder_path_list) 
                     VALUES ('{token}', '{pwhash}', '{folder_list}')""")

        cls.folder_encryption(folder_list)
        conn.commit()
        conn.close()

    # @track
    # @safe_use(retrieval=True)
    @classmethod
    def get_accounts(self):
        if isinstance(self, dbrepository):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute("""SELECT * FROM accounts""")
            result = c.fetchall()
            conn.close()
            return result
        else:
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute("""SELECT * FROM accounts""")
            result = c.fetchall()
            conn.close()
            return result

    # @track
    # @safe_use(retrieval=True)
    @classmethod
    def get_account_by_token(self, token: str) -> str:
        if isinstance(self, dbrepository):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT token, folder_path_list FROM accounts WHERE token='{token}'""")
            result = c.fetchone()
            conn.close()
            return result
        else:
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT token, folder_path_list FROM accounts WHERE token='{token}'""")
            result = c.fetchall()
            conn.close()
            return result

    @classmethod
    def add_account(self, token:str, folder_list: list[str]):
        if isinstance(self, dbrepository):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT folder_path_list FROM accounts WHERE token='{token}'""")
            old_folder_list = c.fetchone()[0]
            new_folder_list = str(old_folder_list).removesuffix(']') + ', "' + str(",".join(folder_list)) + '" ]'
            print(new_folder_list)
            c.execute(f"""UPDATE accounts SET folder_path_list='{new_folder_list}' WHERE token='{token}'""")
            self.folder_encryption(new_folder_list)
            conn.commit()
            conn.close()

        else:
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT folder_path_list FROM accounts WHERE token='{token}'""")
            old_folder_list = c.fetchone()[0]
            new_folder_list = str(old_folder_list).removesuffix(']') + ', "' + str(",".join(folder_list)) + '" ]'
            print(new_folder_list)
            c.execute(f"""UPDATE accounts SET folder_path_list='{new_folder_list}' WHERE token='{token}'""")
            self.folder_encryption(new_folder_list)
            conn.commit()
            conn.close()

    @classmethod
    def access_content(self, token: str, folder_list: list[str]):
        if isinstance(self, dbrepository):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT folder_path_list FROM accounts WHERE token='{token}'""")
            old_folder_list = c.fetchone()[0]
            self.folder_decryption(folder_list)
            new_folder_list = '[' + ', '.join(list(json.loads(old_folder_list)).remove(folder_list))+ ']'
            c.execute(f"""UPDATE accounts SET folder_path_list={new_folder_list} WHERE token='{token}'""")
            conn.commit()
            conn.close
        else:
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT folder_path_list FROM accounts WHERE token='{token}'""")
            old_folder_list = c.fetchone()[0]
            self.folder_decryption(folder_list)
            new_folder_list = '[' + ', '.join(list(json.loads(old_folder_list)).remove(folder_list)) + ']'
            c.execute(f"""UPDATE accounts SET folder_path_list={new_folder_list} WHERE token='{token}'""")
            conn.commit()
            conn.close

    @classmethod
    def delete_account(self, token: str):
        if isinstance(self, dbrepository):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT folder_path_list FROM accounts WHERE token='{token}'""")
            folder_list = c.fetchone()[0]
            self.folder_decryption(folder_list)
            c.execute(f"""DELETE FROM accounts WHERE token='{token}'""")
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT folder_path_list FROM accounts WHERE token='{token}'""")
            folder_list = c.fetchone()[0]
            self.folder_decryption(folder_list)
            c.execute(f"""DELETE FROM accounts WHERE token='{token}'""")
            conn.commit()
            conn.close()

    @classmethod
    def folder_encryption(self, folder_list):
        actual_folder_list = json.loads(folder_list)
        encrypt(actual_folder_list)

    @classmethod
    def folder_decryption(self, folder_list):
        actual_folder_list = json.loads(folder_list)
        decrypt(actual_folder_list)

    @classmethod
    def authenticate(self, token: str, password: str) -> bool:
        if isinstance(self, dbrepository):
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT password_hash FROM accounts WHERE token='{token}'""")
            password_hash = c.fetchone()
            if not password_hash == None:
                if verify.verify(password, password_hash):
                    conn.close()
                    return True
            else:
                raise Exception('INVALID CREDENTIALS')
        else:
            conn = sqlite3.connect('db.sqlite')
            c = conn.cursor()
            c.execute(f"""SELECT password_hash FROM accounts WHERE token='{token}'""")
            password_hash = c.fetchone()[0]
            if not password_hash == None:
                if verify.verify(password, password_hash):
                    conn.close()
                    return True
            else:
                raise Exception('INVALID CREDENTIALS')

