import string
import secrets


def generate_password(
    length=16, use_upper=True, use_lower=True, use_numbers=True, use_symbols=True
):
    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_numbers:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if not pool:
        raise ValueError("At least one character type must be selected.")

    if length < 4 and (use_upper and use_lower and use_numbers and use_symbols):
        raise ValueError("Length must be at least 4 to include all character types.")

    password_chars = []

    if use_upper:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if use_numbers:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice(string.punctuation))

    while len(password_chars) < length:
        password_chars.append(secrets.choice(pool))

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
