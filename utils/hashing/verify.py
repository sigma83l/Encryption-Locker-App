import bcrypt

def verify(password_condidate:str, password_hash:str)->bool:
    res = bcrypt.checkpw(password_condidate.encode('utf-8'), password_hash.encode('utf-8'))
    return res
