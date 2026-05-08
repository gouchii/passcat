import hashlib
import requests


def is_pwned(password:str)->int:

    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    first5_char, tail = sha1_password[:5], sha1_password[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{first5_char}")
        response.raise_for_status()
    except requests.RequestException:
        return -1

    hashes = (line.split(":") for line in response.text.splitlines())

    for h, count in hashes:
        if h == tail:
            return int(count)

    return 0
