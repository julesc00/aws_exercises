import os


def get_os_user_lower() -> str:
    """Return the current OS user in lowercase."""
    username = os.getenv("USER")
    if username is None:
        raise OSError("USER environment variable not set")
    return username.lower()
