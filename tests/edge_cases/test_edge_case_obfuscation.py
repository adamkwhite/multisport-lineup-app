"""
Edge case tests for name obfuscation function
"""

import os
import sys

import pytest

# Add the parent directory to sys.path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app import obfuscate_name


class TestObfuscationEdgeCases:
    """Edge case tests for obfuscate_name function"""

    def test_unicode_emoji_characters(self):
        """Test obfuscation with emoji characters"""
        result = obfuscate_name("John 😀 Smith")
        # Should handle emoji gracefully
        assert result is not None
        assert len(result) > 0

    def test_unicode_chinese_characters(self):
        """Test obfuscation with Chinese characters"""
        result = obfuscate_name("李明")
        # Should obfuscate Chinese names
        assert result is not None
        assert len(result) > 0

    def test_unicode_mixed_languages(self):
        """Test obfuscation with mixed language characters"""
        result = obfuscate_name("José García")
        # Should handle accented characters
        assert result is not None
        assert "é" not in result or "*" in result  # Should obfuscate

    def test_special_characters_at_sign(self):
        """Test obfuscation with @ symbol"""
        result = obfuscate_name("John@Smith")
        assert result is not None
        # Should treat as single name or handle special chars
        assert len(result) > 0

    def test_special_characters_hash(self):
        """Test obfuscation with # symbol"""
        result = obfuscate_name("Player#1 Team")
        assert result is not None
        assert len(result) > 0

    def test_special_characters_dollar(self):
        """Test obfuscation with $ symbol"""
        result = obfuscate_name("Dollar$ Sign")
        assert result is not None
        assert len(result) > 0

    def test_very_long_name(self):
        """Test obfuscation with 100+ character name"""
        long_name = "Christopher" * 10 + " " + "Montgomery" * 10
        result = obfuscate_name(long_name)

        assert result is not None
        # Should obfuscate long names
        assert "*" in result
        # Should still be readable format
        assert " " in result

    def test_extremely_long_single_name(self):
        """Test obfuscation with single word 100+ chars"""
        long_name = "A" * 150
        result = obfuscate_name(long_name)

        assert result is not None
        assert result.startswith("A")
        assert "*" in result
        # Should have many stars for long name
        assert result.count("*") > 100

    def test_hyphenated_first_name(self):
        """Test obfuscation with hyphenated first name"""
        result = obfuscate_name("Mary-Jane Watson")
        assert result is not None
        # Should obfuscate but preserve structure somewhat
        assert "*" in result

    def test_hyphenated_last_name(self):
        """Test obfuscation with hyphenated last name"""
        result = obfuscate_name("John Smith-Jones")
        assert result is not None
        assert "*" in result

    def test_double_hyphenated_name(self):
        """Test obfuscation with multiple hyphens"""
        result = obfuscate_name("Mary-Jane Smith-Jones")
        assert result is not None
        assert "*" in result

    def test_name_with_apostrophe(self):
        """Test obfuscation with apostrophe (O'Brien)"""
        result = obfuscate_name("Patrick O'Brien")
        assert result is not None
        assert "*" in result

    def test_name_with_multiple_spaces(self):
        """Test obfuscation with multiple spaces"""
        result = obfuscate_name("John    Smith")
        assert result is not None
        # Should handle multiple spaces
        assert result != "Unknown Player"

    def test_name_with_tabs(self):
        """Test obfuscation with tab characters"""
        result = obfuscate_name("John\tSmith")
        assert result is not None

    def test_name_with_newlines(self):
        """Test obfuscation with newline characters"""
        result = obfuscate_name("John\nSmith")
        assert result is not None

    def test_three_part_name(self):
        """Test obfuscation with three-part name (verified behavior)"""
        result = obfuscate_name("John William Smith")
        # Takes first and last, per existing test
        assert result == "J*** S****"

    def test_four_part_name(self):
        """Test obfuscation with four-part name"""
        result = obfuscate_name("Mary Jane Watson Parker")
        assert result is not None
        # Should take first and last part
        assert result.startswith("M")
        assert "P" in result

    def test_name_with_suffix(self):
        """Test obfuscation with suffix (Jr., Sr., III)"""
        result = obfuscate_name("John Smith Jr.")
        assert result is not None
        assert "*" in result

    def test_numbers_in_name(self):
        """Test obfuscation with numbers"""
        result = obfuscate_name("Player 42")
        assert result is not None
        assert len(result) > 0

    def test_only_numbers(self):
        """Test obfuscation with only numbers"""
        result = obfuscate_name("123 456")
        assert result is not None
        assert len(result) > 0

    def test_leading_trailing_spaces(self):
        """Test obfuscation with leading/trailing spaces (should strip)"""
        result = obfuscate_name("  John Smith  ")
        # Should strip spaces per existing implementation
        assert result == "J*** S****"

    def test_mixed_case_name(self):
        """Test obfuscation preserves case of first letter"""
        result = obfuscate_name("john smith")
        assert result is not None
        assert result.startswith("j")

        result2 = obfuscate_name("JOHN SMITH")
        assert result2.startswith("J")

    def test_single_character_first_and_last(self):
        """Test obfuscation with single char first and last name"""
        result = obfuscate_name("A B")
        # Per existing test, should return "A B"
        assert result == "A B"

    def test_all_caps_name(self):
        """Test obfuscation with all caps"""
        result = obfuscate_name("JOHN SMITH")
        assert result is not None
        assert result.startswith("J")
        assert "*" in result

    def test_all_lowercase_name(self):
        """Test obfuscation with all lowercase"""
        result = obfuscate_name("john smith")
        assert result is not None
        assert result.startswith("j")
        assert "*" in result
