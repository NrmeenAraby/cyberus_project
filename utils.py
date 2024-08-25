import re
from urllib.parse import urlparse
import bcrypt
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file_size(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0, os.SEEK_SET)
    return file_size <= MAX_FILE_SIZE_BYTES

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode()


def is_password_match(entered_password, stored_hash):
    stored_hash_bytes = stored_hash.encode()

    return bcrypt.checkpw(entered_password.encode(), stored_hash_bytes)


def is_strong_password(password):
    min_length = 8
    require_uppercase = True
    require_lowercase = True
    require_digit = True
    require_special_char = True

    if len(password) < min_length:
        return False

    if require_uppercase and not any(char.isupper() for char in password):
        return False

    if require_lowercase and not any(char.islower() for char in password):
        return False

    if require_digit and not any(char.isdigit() for char in password):
        return False


    if require_special_char and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False


    return True

def is_valid_url(server):
    parsed_url = urlparse(server)
    if parsed_url.scheme not in ['http', 'https']:  # lazm http aw https
        return False
    #only allow port 5000
    whitelist = [5000]
    return parsed_url.port in whitelist
