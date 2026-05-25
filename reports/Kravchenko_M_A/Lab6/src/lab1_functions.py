"""
Модуль для анализа последовательности чисел.
"""


def analyze_numbers(numbers):
    """
    Анализирует последовательность чисел и распределяет их по количеству цифр.

    Args:
        numbers: список целых чисел

    Returns:
        dict: словарь с распределением по количеству цифр
    """
    distribution = {}

    for num in numbers:
        num_digits = len(str(abs(num)))

        if num_digits == 1:
            key = "1-циферные"
        elif num_digits == 2:
            key = "2-циферные"
        elif num_digits == 3:
            key = "3-циферные"
        else:
            key = f"{num_digits}-циферные"

        distribution[key] = distribution.get(key, 0) + 1

    return distribution


def format_distribution(distribution):
    """
    Форматирует распределение в виде списка строк.

    Args:
        distribution: словарь с распределением

    Returns:
        list: список строк для вывода
    """
    result = ["\nРаспределение чисел по количеству цифр:"]
    for category, count in sorted(distribution.items()):
        result.append(f"{category}: {count} шт.")
    return result


def print_distribution(distribution):
    """Выводит распределение чисел в удобном формате."""
    for line in format_distribution(distribution):
        print(line)


def validate_n(n):
    """
    Проверяет корректность введенного N.

    Args:
        n: количество чисел

    Returns:
        bool: True если корректно, иначе False

    Raises:
        ValueError: если n не положительное
    """
    if n <= 0:
        raise ValueError("N должно быть положительным числом")
    return True


def validate_number(num_str):
    """
    Проверяет корректность введенного числа.

    Args:
        num_str: строка с числом

    Returns:
        int: число

    Raises:
        ValueError: если строка не является целым числом
    """
    try:
        return int(num_str)
    except ValueError as exc:
        raise ValueError("Ошибка: введите целое число") from exc


def main():
    """Основная функция программы, обрабатывающая ввод пользователя."""
    try:
        n = int(input("Введите количество чисел N: "))
        validate_n(n)

        numbers = []
        print(f"\nВведите {n} целых чисел (каждое с новой строки):")

        for i in range(n):
            while True:
                try:
                    num_str = input(f"Число {i + 1}: ")
                    num = validate_number(num_str)
                    numbers.append(num)
                    break
                except ValueError as e:
                    print(e)

        distribution = analyze_numbers(numbers)

        print(f"\nИсходная последовательность из {n} чисел:")
        print(numbers)

        print_distribution(distribution)

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
