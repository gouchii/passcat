import re


def check_strength(password:str)->str:
    length = len(password)

    types_count = 0
    if re.search(r"[A-Z]", password):
        types_count += 1
    if re.search(r"[a-z]", password):
        types_count += 1
    if re.search(r"[0-9]", password):
        types_count += 1
    if re.search(r"[^A-Za-z0-9]", password):
        types_count += 1

    if length < 8 or types_count <= 1:
        return "Weak"
    elif length >= 12 and types_count >= 3:
        return "Strong"
    else:
        return "Medium"
