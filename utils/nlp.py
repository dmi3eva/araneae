from typing import *


def is_russian(text: str) -> bool:
    ru_alphabet = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
    size = len(text)
    if size == 0:
        return False
    if text[0] in ru_alphabet or text[-1] in ru_alphabet or text[size // 2] in ru_alphabet:
        return True
    return False