from zxcvbn import zxcvbn


def analyze_password(password: str) -> dict:

    result = zxcvbn(password)

    score = result["score"]


    return {
        "score": score,
        "guesses": result["guesses"],
        "feedback": result["feedback"],
        "crack_times": result["crack_times_display"],
        "sequence": result["sequence"],
    }