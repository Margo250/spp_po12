"""
Тесты для функций из лабораторной работы №1.
Файл: test_lab1.py
"""

import pytest
from lab1_functions import analyze_numbers, format_distribution, validate_n, validate_number


class TestAnalyzeNumbers:
    """Тесты для функции analyze_numbers."""

    def test_empty_list(self):
        """Тест пустого списка."""
        result = analyze_numbers([])
        assert not result

    def test_single_digit_numbers(self):
        """Тест одноциферных чисел."""
        result = analyze_numbers([1, 2, 3])
        assert result == {"1-циферные": 3}

    def test_two_digit_numbers(self):
        """Тест двуциферных чисел."""
        result = analyze_numbers([10, 25, 99])
        assert result == {"2-циферные": 3}

    def test_three_digit_numbers(self):
        """Тест трехциферных чисел."""
        result = analyze_numbers([100, 555, 999])
        assert result == {"3-циферные": 3}

    def test_mixed_digits(self):
        """Тест смешанных чисел."""
        result = analyze_numbers([5, 23, 456, 7890, 1])
        # fmt: off
        assert result == {"1-циферные": 2, "2-циферные": 1, "3-циферные": 1, "4-циферные": 1}
        # fmt: on

    def test_negative_numbers(self):
        """Тест отрицательных чисел."""
        result = analyze_numbers([-5, -23, -456])
        assert result == {"1-циферные": 1, "2-циферные": 1, "3-циферные": 1}

    def test_zero(self):
        """Тест нуля."""
        result = analyze_numbers([0])
        assert result == {"1-циферные": 1}

    def test_large_numbers(self):
        """Тест больших чисел."""
        result = analyze_numbers([10000, 100000, 1000000])
        assert result == {"5-циферные": 1, "6-циферные": 1, "7-циферные": 1}

    def test_mixed_positive_and_negative(self):
        """Тест смешанных положительных и отрицательных."""
        result = analyze_numbers([-10, 5, -999, 42, -7])
        assert result == {"1-циферные": 2, "2-циферные": 2, "3-циферные": 1}


class TestFormatDistribution:
    """Тесты для функции format_distribution."""

    def test_empty_distribution(self):
        """Тест пустого распределения."""
        result = format_distribution({})
        assert result == ["\nРаспределение чисел по количеству цифр:"]

    def test_single_category(self):
        """Тест одной категории."""
        result = format_distribution({"1-циферные": 5})
        expected = ["\nРаспределение чисел по количеству цифр:", "1-циферные: 5 шт."]
        assert result == expected

    def test_multiple_categories(self):
        """Тест нескольких категорий."""
        result = format_distribution({"1-циферные": 2, "2-циферные": 3, "3-циферные": 1})
        expected = [
            "\nРаспределение чисел по количеству цифр:",
            "1-циферные: 2 шт.",
            "2-циферные: 3 шт.",
            "3-циферные: 1 шт.",
        ]
        assert result == expected

    def test_sorted_order(self):
        """Тест сортировки категорий."""
        result = format_distribution({"3-циферные": 1, "1-циферные": 2, "2-циферные": 3})
        categories = [line.split(":")[0] for line in result[1:]]
        assert categories == ["1-циферные", "2-циферные", "3-циферные"]


class TestValidateN:
    """Тесты для функции validate_n."""

    def test_valid_positive(self):
        """Тест корректного положительного N."""
        assert validate_n(5) is True
        assert validate_n(1) is True
        assert validate_n(100) is True

    def test_zero_raises_error(self):
        """Тест N=0 вызывает исключение."""
        with pytest.raises(ValueError, match="N должно быть положительным числом"):
            validate_n(0)

    def test_negative_raises_error(self):
        """Тест отрицательного N вызывает исключение."""
        with pytest.raises(ValueError, match="N должно быть положительным числом"):
            validate_n(-5)

    @pytest.mark.parametrize("invalid_n", [-100, -1, 0])
    def test_invalid_values(self, invalid_n):
        """Параметризованный тест невалидных значений."""
        with pytest.raises(ValueError, match="N должно быть положительным числом"):
            validate_n(invalid_n)


class TestValidateNumber:
    """Тесты для функции validate_number."""

    def test_valid_integer(self):
        """Тест корректного целого числа."""
        assert validate_number("123") == 123
        assert validate_number("-456") == -456
        assert validate_number("0") == 0

    def test_float_raises_error(self):
        """Тест вещественного числа вызывает исключение."""
        with pytest.raises(ValueError, match="Ошибка: введите целое число"):
            validate_number("3.14")

    def test_string_raises_error(self):
        """Тест строки вызывает исключение."""
        with pytest.raises(ValueError, match="Ошибка: введите целое число"):
            validate_number("abc")

    def test_empty_string_raises_error(self):
        """Тест пустой строки вызывает исключение."""
        with pytest.raises(ValueError, match="Ошибка: введите целое число"):
            validate_number("")

    # fmt: off
    @pytest.mark.parametrize("invalid_input", ["12.5", "one", "1a2", "", "   ", "1,5"])
    # fmt: on
    def test_invalid_inputs(self, invalid_input):
        """Параметризованный тест невалидных вводов."""
        with pytest.raises(ValueError, match="Ошибка: введите целое число"):
            validate_number(invalid_input)


class TestEdgeCases:
    """Тесты граничных случаев."""

    def test_single_number(self):
        """Тест одного числа."""
        result = analyze_numbers([42])
        assert result == {"2-циферные": 1}

    def test_many_numbers_same_digit_length(self):
        """Тест многих чисел одной разрядности."""
        numbers = list(range(10, 100))
        result = analyze_numbers(numbers)
        assert result == {"2-циферные": 90}

    def test_very_large_number(self):
        """Тест очень большого числа."""
        result = analyze_numbers([1234567890])
        assert result == {"10-циферные": 1}

    def test_very_small_negative(self):
        """Тест очень маленького отрицательного числа."""
        result = analyze_numbers([-999999999])
        assert result == {"9-циферные": 1}

    def test_mixed_all_categories(self):
        """Тест всех категорий разом."""
        numbers = [5, 42, 123, 1000, 10000]
        # fmt: off
        assert analyze_numbers(numbers) == {
            "1-циферные": 1,
            "2-циферные": 1,
            "3-циферные": 1,
            "4-циферные": 1,
            "5-циферные": 1
        }
        # fmt: on
