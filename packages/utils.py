import random
import string

def get_random_string(k: int = 1) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(k)])
