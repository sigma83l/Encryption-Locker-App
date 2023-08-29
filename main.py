from connect.repository import dbrepository
from utils.hashing import hash
from utils.cryptography.encrypt import encrypt
from utils.cryptography.decrypt import decrypt
from account_management.controller import account_controller
import pretty_errors
import app

if __name__ == '__main__':
    options ={'options':'console'}
    app.run(options)()

"~/Documents/program/python programing/folder-locker"