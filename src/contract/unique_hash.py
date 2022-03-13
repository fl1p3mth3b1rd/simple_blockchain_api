from uuid import uuid1
from random import randint


def generate_hash() -> str:
    """Генерирует случайную строку из букв и цифр длиной 20"""
    s = str(uuid1()).replace("-", "")
    rand_ints = [randint(17, 31) for _ in range(4)]
    return s[:16] + s[rand_ints[0]] + s[rand_ints[1]] + \
        s[rand_ints[2]] + s[rand_ints[3]]
