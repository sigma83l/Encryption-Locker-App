import bcrypt

def hash(pwstring):
    salt = bcrypt.gensalt(10)
    return bcrypt.hashpw(pwstring, salt)