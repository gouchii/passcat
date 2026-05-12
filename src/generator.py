import secrets
import string


def generate_password(
    length=16,
    use_upper=True,
    use_lower=True,
    use_numbers=True,
    use_symbols=True,
    min_numbers=1,
    min_symbols=1,
):

    password_chars = []
    pool = ""

    if use_upper:
        pool += string.ascii_uppercase
        password_chars.append(
            secrets.choice(string.ascii_uppercase)
        )

    if use_lower:
        pool += string.ascii_lowercase
        password_chars.append(
            secrets.choice(string.ascii_lowercase)
        )

    if use_numbers:
        pool += string.digits

        for _ in range(min_numbers):
            password_chars.append(
                secrets.choice(string.digits)
            )

    if use_symbols:
        pool += string.punctuation

        for _ in range(min_symbols):
            password_chars.append(
                secrets.choice(string.punctuation)
            )

    if not pool:
        raise ValueError(
            "At least one character type must be selected."
        )

    minimum_required = (
        (1 if use_upper else 0)
        + (1 if use_lower else 0)
        + (min_numbers if use_numbers else 0)
        + (min_symbols if use_symbols else 0)
    )

    if length < minimum_required:
        raise ValueError(
            f"Length must be at least {minimum_required}."
        )

    while len(password_chars) < length:
        password_chars.append(
            secrets.choice(pool)
        )

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)