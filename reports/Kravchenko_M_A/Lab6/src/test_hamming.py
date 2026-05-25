"""
Тесты для функции hammingDistance.
Файл: test_hamming.py
"""

import pytest
from hamming import hamming_distance


class TestHammingDistance:
    """Тесты для функции hamming_distance."""

    # Тесты на исключения и ошибки
    def test_both_none(self):
        """Тест: hammingDistance(None, None) = TypeError."""
        with pytest.raises(TypeError):
            hamming_distance(None, None)

    def test_first_none(self):
        """Тест: hammingDistance(None, *) = -1."""
        result = hamming_distance(None, "abc")
        assert result == -1

    def test_second_none(self):
        """Тест: hammingDistance(*, None) = -1."""
        result = hamming_distance("abc", None)
        assert result == -1

    def test_different_lengths(self):
        """Тест: hammingDistance("abc", " abcd ") = ValueError."""
        with pytest.raises(ValueError, match="Строки должны быть одинаковой длины"):
            hamming_distance("abc", "abcd")

    def test_different_lengths_with_spaces(self):
        """Тест: строки разной длины с пробелами."""
        with pytest.raises(ValueError, match="Строки должны быть одинаковой длины"):
            hamming_distance("abc", " abcd ")

    # Тесты на корректные значения
    def test_both_empty(self):
        """Тест: hammingDistance("", "") = 0."""
        result = hamming_distance("", "")
        assert result == 0

    def test_same_string(self):
        """Тест: hammingDistance(" father ", " father ") = 0."""
        result = hamming_distance(" father ", " father ")
        assert result == 0

    def test_one_difference(self):
        """Тест: hammingDistance("pip", " pop ") = 1."""
        result = hamming_distance("pip", "pop")
        assert result == 1

    def test_two_differences(self):
        """Тест: hammingDistance(" abcd ", " abab ") = 2."""
        result = hamming_distance("abcd", "abab")
        assert result == 2

    def test_one_difference_hello_hallo(self):
        """Тест: hammingDistance(" hello ", " hallo ") = 1."""
        result = hamming_distance("hello", "hallo")
        assert result == 1

    def test_all_different(self):
        """Тест: hammingDistance(" abcd ", " efgi ") = 4."""
        result = hamming_distance("abcd", "efgi")
        assert result == 4

    def test_case_sensitive(self):
        """Тест: регистр имеет значение."""
        result = hamming_distance("Hello", "hello")
        assert result == 1

    def test_numbers_as_strings(self):
        """Тест: строки из цифр."""
        result = hamming_distance("12345", "12345")
        assert result == 0

    def test_mixed_characters(self):
        """Тест: смешанные символы."""
        result = hamming_distance("a1b2c", "a1b3c")
        assert result == 1

    def test_long_strings(self):
        """Тест: длинные строки."""
        str1 = "a" * 1000
        str2 = "a" * 500 + "b" * 500
        result = hamming_distance(str1, str2)
        assert result == 500

    def test_special_characters(self):
        """Тест: специальные символы."""
        result = hamming_distance("!@#$%", "!@#$$")
        assert result == 1


class TestHammingDistanceEdgeCases:
    """Тесты граничных случаев."""

    def test_single_char_same(self):
        """Тест: один символ, одинаковые."""
        result = hamming_distance("a", "a")
        assert result == 0

    def test_single_char_different(self):
        """Тест: один символ, разные."""
        result = hamming_distance("a", "b")
        assert result == 1

    def test_spaces_only(self):
        """Тест: только пробелы."""
        result = hamming_distance("   ", "   ")
        assert result == 0

    def test_empty_vs_empty_string(self):
        """Тест: пустые строки."""
        result = hamming_distance("", "")
        assert result == 0

    def test_unicode_characters(self):
        """Тест: юникод символы."""
        result = hamming_distance("привет", "привет")
        assert result == 0

    def test_unicode_different(self):
        """Тест: разные юникод символы."""
        result = hamming_distance("привет", "превет")
        assert result == 1
