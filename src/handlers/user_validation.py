import re


def validate_fio(fio: str) -> bool:
    """
    Validates a given string as a valid FIO (First Name + Initials + Last Name).

    Args:
        fio (str): The string to validate.

    Returns:
        bool: True if the string is a valid FIO, False otherwise.
    """

    # Split the string by spaces to get the individual words.
    words = fio.split()

    # Check if the string has at least two words.
    if len(words) < 2:
        return False

    # Check if the first letter of each word is uppercase.
    for word in words:
        if not word[0].isupper():
            return False

    # If all checks pass, the string is a valid FIO.
    return True


def validate_phone_number(phone_number: str) -> bool:
    pattern = r"^7\d{10}$"
    if re.match(pattern, phone_number):
        return True
    else:
        return False


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        return True
    else:
        return False
