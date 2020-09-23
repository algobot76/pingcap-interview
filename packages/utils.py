import random
import string


def get_random_string(k: int = 1) -> str:
    """Returns a random string of length k.

    Args:
        k: Length of a string (default: 1).

    Returns:
        A random string.
    """

    return ''.join([random.choice(string.ascii_letters) for _ in range(k)])
