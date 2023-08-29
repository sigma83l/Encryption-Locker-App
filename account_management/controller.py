from connect.repository import dbrepository
from utils.hashing import hash
import json


class account_controller:
    def __init__(self, token: str, password: str, folder_list: list[str]):
        self._token = token
        self._pwhash = (hash.hash(password.encode('utf-8'))).decode('utf-8')
        self._folder_list = json.dumps(folder_list)
        self._db = dbrepository

    def create(self) -> None:
        self._db.create_account(self._token, self._pwhash, self._folder_list)

    def read(self) -> list[str]:
        return self._db.get_accounts()

    def read_by_token(self, token: str) -> str:
        return self._db.get_account_by_token(token)

    def add_account(self, token: str, password: str, folder_list:list[str]) -> None:
        if self._db.authenticate(token, password):
            self._db.add_account(token, folder_list)
            # print('yes')
        else:
            raise Exception('INVALID CREDENTIALS')
            # print('no')

    def access(self, token:str, password: str, folder_list:list[str]):
        if self._db.authenticate(token, password):
            self._db.access_content()
            # print('yes')
        else:
            raise Exception('INVALID CREDENTIALS')
            # print('no')

    def delete_account(self, token: str, password: str):
        if self._db.authenticate(token, password):
            self._db.delete_account()
            # print('yes')
        else:
            raise Exception('INVALID CREDENTIALS')
            # print('no')