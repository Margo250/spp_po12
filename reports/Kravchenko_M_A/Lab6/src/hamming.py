"""
Модуль для вычисления расстояния Хэмминга.
Файл: hamming.py
"""


def hamming_distance(str1: str, str2: str) -> int:
    """
    Вычисляет расстояние Хэмминга между двумя строками.

    Расстояние Хэмминга - это количество позиций, в которых символы
    двух строк одинаковой длины различаются.

    Args:
        str1: первая строка
        str2: вторая строка

    Returns:
        int: расстояние Хэмминга

    Raises:
        TypeError: если оба аргумента None
        ValueError: если строки разной длины

    Спецификация:
        hammingDistance(None, None) = TypeError
        hammingDistance(None, *) = -1
        hammingDistance(*, None) = -1
        hammingDistance("abc", "abcd") = ValueError
        hammingDistance("", "") = 0
        hammingDistance("father", "father") = 0
        hammingDistance("pip", "pop") = 1
        hammingDistance("abcd", "abab") = 2
        hammingDistance("hello", "hallo") = 1
        hammingDistance("abcd", "efgi") = 4
    """
    # Случай: оба аргумента None
    if str1 is None and str2 is None:
        raise TypeError("Both arguments cannot be None")

    # Случай: первый аргумент None
    if str1 is None:
        return -1

    # Случай: второй аргумент None
    if str2 is None:
        return -1

    # Случай: строки разной длины
    if len(str1) != len(str2):
        raise ValueError("Строки должны быть одинаковой длины")

    # Вычисление расстояния Хэмминга
    distance = 0
    for idx, char1 in enumerate(str1):
        if char1 != str2[idx]:
            distance += 1

    return distance
