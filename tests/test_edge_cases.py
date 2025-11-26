import unittest
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add the parent directory to the path so we can import bingo_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bingo_generator
import bingo_card


class TestFileOperations(unittest.TestCase):
    """Test file operations and edge cases."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_read_entries_with_special_characters(self):
        """Test reading entries with special characters and formatting."""
        special_entries = [
            "Line with trailing spaces   ",
            "  Line with leading spaces",
            "Line with \"quotes\"",
            "Line with 'single quotes'",
            "Line with symbols: @#$%^&*()",
            "Line with numbers: 123456",
            "Multi-word entry with spaces",
            "Hyphenated-entry",
            "Entry.with.periods",
            "Entry/with/slashes"
        ]
        
        test_file = "special_entries.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            for entry in special_entries:
                f.write(f"{entry}\n")
        
        entries = bingo_generator.read_lines(test_file)
        
        # Check that whitespace is stripped
        expected = [entry.strip() for entry in special_entries]
        self.assertEqual(entries, expected)

    def test_read_entries_large_file(self):
        """Test reading a large number of entries."""
        large_entries = [f"Entry number {i}" for i in range(1000)]
        
        test_file = "large_entries.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            for entry in large_entries:
                f.write(f"{entry}\n")
        
        entries = bingo_generator.read_lines(test_file)
        
        self.assertEqual(len(entries), 1000)
        self.assertEqual(entries[0], "Entry number 0")
        self.assertEqual(entries[999], "Entry number 999")

    def test_read_entries_mixed_encoding(self):
        """Test reading entries with various Unicode characters."""
        mixed_entries = [
            "English entry",
            "Entrée française",
            "Entrada española", 
            "Deutsche Eingabe",
            "日本語エントリー",
            "Русская запись",
            "العربية دخول",
            "Emoji entry 🎉🎊🎈"
        ]
        
        test_file = "mixed_encoding.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            for entry in mixed_entries:
                f.write(f"{entry}\n")
        
        entries = bingo_generator.read_lines(test_file)
        self.assertEqual(entries, mixed_entries)

    def test_read_entries_empty_file(self):
        """Test reading from an empty file."""
        test_file = "empty.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            pass  # Create empty file
        
        entries = bingo_generator.read_lines(test_file)
        self.assertEqual(entries, [])

    def test_read_entries_only_whitespace(self):
        """Test reading from a file with only whitespace."""
        test_file = "whitespace.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("   \n")
            f.write("\t\t\n")
            f.write("\n")
            f.write("    \t   \n")
        
        entries = bingo_generator.read_lines(test_file)
        self.assertEqual(entries, [])


class TestBingoCardGeneration(unittest.TestCase):
    """Test bingo card generation edge cases and scenarios."""

    def test_generate_single_entry_card(self):
        """Test generating a card with a single entry."""
        entries = ["Single entry"]
        card = bingo_card.generate_bingo_card(entries, 1)
        
        self.assertEqual(len(card), 1)
        self.assertEqual(card[0], "Single entry")

    def test_generate_card_randomness(self):
        """Test that card generation produces different results."""
        entries = [f"Entry {i}" for i in range(50)]
        num_entries = 10
        
        # Generate multiple cards
        cards = []
        for _ in range(20):
            card = bingo_card.generate_bingo_card(entries, num_entries)
            cards.append(tuple(sorted(card)))  # Sort for comparison
        
        # Check that we get different combinations
        unique_cards = set(cards)
        self.assertGreater(len(unique_cards), 1, "Cards should be different due to randomness")

    def test_generate_card_with_duplicate_source_entries(self):
        """Test card generation when source has duplicate entries."""
        # This shouldn't happen in normal usage, but test the behavior
        entries = ["Entry 1", "Entry 2", "Entry 1", "Entry 3", "Entry 2"]
        
        # The function should still work, but behavior may vary
        # depending on how random.sample handles duplicates
        try:
            card = bingo_card.generate_bingo_card(entries, 3)
            self.assertLessEqual(len(card), 3)
        except ValueError:
            # This is also acceptable behavior
            pass

    def test_generate_card_boundary_conditions(self):
        """Test card generation at boundary conditions."""
        entries = ["A", "B", "C", "D", "E"]
        
        # Test with exact number of entries
        card = bingo_card.generate_bingo_card(entries, 5)
        self.assertEqual(len(card), 5)
        self.assertEqual(set(card), set(entries))
        
        # Test with one less than available
        card = bingo_card.generate_bingo_card(entries, 4)
        self.assertEqual(len(card), 4)
        self.assertTrue(set(card).issubset(set(entries)))


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_read_entries_permission_denied(self):
        """Test handling of permission denied errors."""
        # Skip this test on Windows where chmod doesn't work the same way
        if os.name == 'nt':
            self.skipTest("Permission test not applicable on Windows")
        
        test_file = "no_permission.txt"
        with open(test_file, "w") as f:
            f.write("Entry 1\n")
        
        # Remove read permission
        os.chmod(test_file, 0o000)
        
        try:
            # read_lines should handle permission errors gracefully and return empty list
            entries = bingo_generator.read_lines(test_file)
            self.assertEqual(entries, [])
        finally:
            # Restore permissions for cleanup
            os.chmod(test_file, 0o644)

    def test_generate_card_negative_entries(self):
        """Test card generation with negative number of entries."""
        entries = ["A", "B", "C"]
        
        with self.assertRaises(ValueError):
            bingo_card.generate_bingo_card(entries, -1)

    def test_generate_card_empty_source(self):
        """Test card generation with empty source entries."""
        entries = []
        
        # Requesting 0 entries should work
        card = bingo_card.generate_bingo_card(entries, 0)
        self.assertEqual(card, [])
        
        # Requesting any positive number should fail
        with self.assertRaises(ValueError):
            bingo_card.generate_bingo_card(entries, 1)


if __name__ == '__main__':
    unittest.main()
