import hashlib
import database
import re


def check_login(email, password):
    user = database.get_user_by_email(email)
    if not user:
        return False

    stored_hash = user[3]
    entered_hash = hashlib.sha256(password.encode()).hexdigest()

    return stored_hash == entered_hash


def is_valid_email(email):
    pattern = r"^[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email)


def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True


def email_exists(email):
    user = database.get_user_by_email(email)
    return user is not None


def is_valid_name(name):
    return bool(re.match(r"^[A-Za-z ]+$", name))