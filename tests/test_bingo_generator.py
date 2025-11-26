import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# Add the parent directory to the path so we can import bingo_generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bingo_generator
import pdf_generator
import bingo_card


class TestBingoGenerator(unittest.TestCase):
    """Test cases for the bingo generator functions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.temp_dir = self.test_dir  # Add this for backward compatibility
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Sample test entries
        self.sample_entries = [
            "Sorry, I was on mute",
            "Can you hear me?",
            "Let's take this offline",
            "Circle back",
            "Touch base",
            "Action items",
            "Low hanging fruit",
            "Synergy",
            "Think outside the box",
            "Bandwidth"
        ]
        
        # Create a test entries file
        self.test_entries_file = "test_entries.txt"
        self.temp_entries_file = self.test_entries_file  # Add this for backward compatibility
        with open(self.test_entries_file, "w", encoding="utf-8") as f:
            for entry in self.sample_entries:
                f.write(f"{entry}\n")

    def tearDown(self):
        """Clean up after each test method."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_read_entries_valid_file(self):
        """Test reading entries from a valid file."""
        entries = bingo_generator.read_lines(self.test_entries_file)
        
        self.assertEqual(len(entries), len(self.sample_entries))
        self.assertEqual(entries, self.sample_entries)

    def test_read_lines_with_empty_lines(self):
        """Test that empty lines are properly filtered out."""
        test_content = "entry1\n\nentry2\n   \nentry3\n"
        with open(self.temp_entries_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        entries = bingo_generator.read_lines(self.temp_entries_file)
        self.assertEqual(entries, ["entry1", "entry2", "entry3"])
    
    def test_read_lines_nonexistent_file(self):
        """Test reading from a non-existent file returns empty list."""
        entries = bingo_generator.read_lines("nonexistent_file.txt")
        self.assertEqual(entries, [])
    
    def test_read_lines_participants_file(self):
        """Test reading participants file."""
        test_participants = "Aaron\nDiogo\nGermano\nJessica\nPriscilla\nVinicius\n"
        temp_participants_file = os.path.join(self.temp_dir, "participants.txt")
        with open(temp_participants_file, "w", encoding="utf-8") as f:
            f.write(test_participants)
        
        participants = bingo_generator.read_lines(temp_participants_file)
        expected = ["Aaron", "Diogo", "Germano", "Jessica", "Priscilla", "Vinicius"]
        self.assertEqual(participants, expected)

    def test_read_entries_nonexistent_file(self):
        """Test reading entries from a nonexistent file."""
        entries = bingo_generator.read_lines("nonexistent.txt")
        self.assertEqual(entries, [])

    def test_generate_bingo_card_valid_input(self):
        """Test generating a bingo card with valid input."""
        entries = self.sample_entries
        num_entries = 5
        
        card = bingo_card.generate_bingo_card(entries, num_entries)
        
        self.assertEqual(len(card), num_entries)
        self.assertTrue(all(entry in entries for entry in card))
        self.assertEqual(len(set(card)), num_entries)  # No duplicates

    def test_generate_bingo_card_all_entries(self):
        """Test generating a bingo card with all available entries."""
        entries = self.sample_entries
        num_entries = len(entries)
        
        card = bingo_card.generate_bingo_card(entries, num_entries)
        
        self.assertEqual(len(card), num_entries)
        self.assertEqual(set(card), set(entries))

    def test_generate_bingo_card_too_many_entries(self):
        """Test generating a bingo card with more entries than available."""
        entries = self.sample_entries
        num_entries = len(entries) + 1
        
        with self.assertRaises(ValueError):
            bingo_card.generate_bingo_card(entries, num_entries)

    def test_generate_bingo_card_zero_entries(self):
        """Test generating a bingo card with zero entries."""
        entries = self.sample_entries
        num_entries = 0
        
        card = bingo_card.generate_bingo_card(entries, num_entries)
        
        self.assertEqual(len(card), 0)
        self.assertEqual(card, [])

    @patch('pdf_generator.canvas.Canvas')
    def test_save_card_as_pdf_basic_functionality(self, mock_canvas_class):
        """Test basic PDF creation functionality with new signature."""
        mock_canvas = mock_canvas_class.return_value
        
        card_entries = ["Entry 1", "Entry 2", "Entry 3", "Entry 4"]
        filename = "test_card.pdf"
        card_title = "Test Bingo Card"
        
        pdf_generator.save_card_as_pdf(card_entries, filename, card_title)
        
        # Check that canvas was created with correct parameters
        mock_canvas_class.assert_called_once_with(filename, pagesize=letter)
        
        # Check that save was called
        mock_canvas.save.assert_called_once()

    @patch('pdf_generator.canvas.Canvas')
    def test_save_card_as_pdf_with_checkboxes(self, mock_canvas_class):
        """Test PDF creation with interactive checkboxes."""
        mock_canvas = mock_canvas_class.return_value
        mock_acroform = mock_canvas.acroForm
        
        entries = ["Entry 1", "Entry 2", "Entry 3", "Entry 4"]
        filename = "test_card.pdf"
        title = "Test Bingo Card"
        
        pdf_generator.save_card_as_pdf(entries, filename, title)
        
        # Verify canvas was created with correct parameters
        mock_canvas_class.assert_called_once_with(filename, pagesize=letter)
        
        # Verify title was drawn
        mock_canvas.setFont.assert_any_call("Helvetica-Bold", 16)
        mock_canvas.drawCentredString.assert_called()
        
        # Verify checkboxes were created for each entry
        self.assertEqual(mock_acroform.checkbox.call_count, len(entries))
        
        # Verify checkbox parameters
        checkbox_calls = mock_acroform.checkbox.call_args_list
        for i, call in enumerate(checkbox_calls):
            args, kwargs = call
            self.assertEqual(kwargs['name'], f"cb_{i}")
            self.assertEqual(kwargs['tooltip'], entries[i])
            self.assertEqual(kwargs['size'], 12)
            self.assertEqual(kwargs['buttonStyle'], 'check')
            self.assertEqual(kwargs['borderColor'], colors.black)
            self.assertEqual(kwargs['fillColor'], colors.white)
            self.assertEqual(kwargs['textColor'], colors.black)
            self.assertTrue(kwargs['forceBorder'])
        
        # Verify text was drawn for each entry
        self.assertEqual(mock_canvas.drawString.call_count, len(entries))
        
        # Verify grid layout (cells and borders)
        expected_cells = len(entries)
        self.assertEqual(mock_canvas.rect.call_count, expected_cells)
        
        # Verify canvas was saved
        mock_canvas.save.assert_called_once()

    @patch('pdf_generator.canvas.Canvas')
    def test_save_card_as_pdf_grid_layout(self, mock_canvas_class):
        """Test that PDF uses proper grid layout for different numbers of entries."""
        mock_canvas = mock_canvas_class.return_value
        
        # Test with 9 entries (should be 3x3 grid)
        entries_9 = [f"Entry {i}" for i in range(1, 10)]
        pdf_generator.save_card_as_pdf(entries_9, "test_9.pdf", "Test Card")
        
        # Should have 9 rectangles (one per cell) and 9 checkboxes
        self.assertEqual(mock_canvas.rect.call_count, 9)
        self.assertEqual(mock_canvas.acroForm.checkbox.call_count, 9)
        
        # Reset mocks for next test
        mock_canvas.reset_mock()
        mock_canvas.acroForm.reset_mock()
        
        # Test with 16 entries (should be 4x4 grid)
        entries_16 = [f"Entry {i}" for i in range(1, 17)]
        pdf_generator.save_card_as_pdf(entries_16, "test_16.pdf", "Test Card")
        
        # Should have 16 rectangles and 16 checkboxes
        self.assertEqual(mock_canvas.rect.call_count, 16)
        self.assertEqual(mock_canvas.acroForm.checkbox.call_count, 16)

    @patch('pdf_generator.canvas.Canvas')
    def test_save_card_as_pdf_unicode_entries(self, mock_canvas_class):
        """Test PDF creation with Unicode characters in entries."""
        mock_canvas = mock_canvas_class.return_value
        
        unicode_entries = ["Café meeting ☕", "Résumé review 📄", "Naïve approach 🤔"]
        filename = "unicode_test.pdf"
        title = "Unicode Test Card"
        
        pdf_generator.save_card_as_pdf(unicode_entries, filename, title)
        
        # Verify checkboxes were created with Unicode tooltips
        checkbox_calls = mock_canvas.acroForm.checkbox.call_args_list
        for i, call in enumerate(checkbox_calls):
            args, kwargs = call
            self.assertEqual(kwargs['tooltip'], unicode_entries[i])
        
        # Verify Unicode text was drawn
        text_calls = mock_canvas.drawString.call_args_list
        self.assertEqual(len(text_calls), len(unicode_entries))

    @patch('pdf_generator.canvas.Canvas')
    @patch('builtins.print')
    def test_save_card_as_pdf_print_confirmation(self, mock_print, mock_canvas_class):
        """Test that save confirmation is printed."""
        mock_canvas = mock_canvas_class.return_value
        
        entries = ["Entry 1", "Entry 2"]
        filename = "test_print.pdf"
        title = "Test Card"
        
        pdf_generator.save_card_as_pdf(entries, filename, title)
        
        # Verify confirmation message was printed
        mock_print.assert_called_once_with(f"Saved: {filename}")

    @patch('pdf_generator.canvas.Canvas')
    def test_save_card_as_pdf_font_settings(self, mock_canvas_class):
        """Test that correct fonts are applied."""
        mock_canvas = mock_canvas_class.return_value
        
        entries = ["Entry 1", "Entry 2"]
        filename = "font_test.pdf"
        title = "Font Test Card"
        
        pdf_generator.save_card_as_pdf(entries, filename, title)
        
        # Verify font settings
        font_calls = mock_canvas.setFont.call_args_list
        
        # Should have at least two font calls: one for title (Helvetica-Bold, 16) and one for entries (Helvetica, 9)
        title_font_call = None
        entry_font_call = None
        
        for call in font_calls:
            args = call[0]
            if args == ("Helvetica-Bold", 16):
                title_font_call = call
            elif args == ("Helvetica", 9):
                entry_font_call = call
        
        self.assertIsNotNone(title_font_call, "Title font (Helvetica-Bold, 16) should be set")
        self.assertIsNotNone(entry_font_call, "Entry font (Helvetica, 9) should be set")

    def test_save_card_as_pdf_filename_generation(self):
        """Test that different filenames and titles work correctly."""
        test_cases = [
            (["Entry 1"], "custom_card.pdf", "Custom Title"),
            (["A", "B"], "another_file.pdf", "Another Title"),
            (["Test"], "test.pdf", "Test Card")
        ]
        
        for entries, filename, title in test_cases:
            with patch('pdf_generator.canvas.Canvas') as mock_canvas_class:
                pdf_generator.save_card_as_pdf(entries, filename, title)
                mock_canvas_class.assert_called_once_with(filename, pagesize=letter)


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function and command-line interface."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test entries file
        self.entries_file = bingo_generator.ENTRIES_FILE
        sample_entries = [f"Entry {i}" for i in range(1, 21)]
        with open(self.entries_file, "w", encoding="utf-8") as f:
            for entry in sample_entries:
                f.write(f"{entry}\n")

    def tearDown(self):
        """Clean up after tests."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch('sys.argv', ['bingo_generator.py', '5', '2'])
    @patch('bingo_generator.save_card_as_pdf')
    def test_main_without_participants(self, mock_save_pdf):
        """Test main function without participants file."""
        bingo_generator.main()
        
        # Should call save_card_as_pdf twice (for 2 cards)
        self.assertEqual(mock_save_pdf.call_count, 2)
        
        # Check that generic filenames are used
        calls = mock_save_pdf.call_args_list
        self.assertEqual(calls[0][0][1], "bingo_card_1.pdf")
        self.assertEqual(calls[0][0][2], "Bingo Card #1")
        self.assertEqual(calls[1][0][1], "bingo_card_2.pdf")
        self.assertEqual(calls[1][0][2], "Bingo Card #2")

    @patch('sys.argv', ['bingo_generator.py', '5', '3'])
    @patch('bingo_generator.save_card_as_pdf')
    def test_main_with_participants(self, mock_save_pdf):
        """Test main function with participants file."""
        # Create participants file
        participants_content = "Aaron\nDiogo\nGermano\n"
        with open(bingo_generator.PARTICIPANTS_FILE, "w", encoding="utf-8") as f:
            f.write(participants_content)
        
        bingo_generator.main()
        
        # Should call save_card_as_pdf three times (for 3 cards)
        self.assertEqual(mock_save_pdf.call_count, 3)
        
        # Check that participant names are used
        calls = mock_save_pdf.call_args_list
        self.assertEqual(calls[0][0][1], "bingo_card_Aaron.pdf")
        self.assertEqual(calls[0][0][2], "Bingo Card - Aaron")
        self.assertEqual(calls[1][0][1], "bingo_card_Diogo.pdf")
        self.assertEqual(calls[1][0][2], "Bingo Card - Diogo")
        self.assertEqual(calls[2][0][1], "bingo_card_Germano.pdf")
        self.assertEqual(calls[2][0][2], "Bingo Card - Germano")

    @patch('sys.argv', ['bingo_generator.py', '4', '5'])
    @patch('bingo_generator.save_card_as_pdf')
    def test_main_more_cards_than_participants(self, mock_save_pdf):
        """Test main function when requesting more cards than participants."""
        # Create participants file with only 2 people
        participants_content = "Aaron\nDiogo\n"
        with open(bingo_generator.PARTICIPANTS_FILE, "w", encoding="utf-8") as f:
            f.write(participants_content)
        
        bingo_generator.main()
        
        # Should call save_card_as_pdf five times (for 5 cards)
        self.assertEqual(mock_save_pdf.call_count, 5)
        
        # Check that first 2 use participant names, rest use generic names
        calls = mock_save_pdf.call_args_list
        self.assertEqual(calls[0][0][1], "bingo_card_Aaron.pdf")
        self.assertEqual(calls[0][0][2], "Bingo Card - Aaron")
        self.assertEqual(calls[1][0][1], "bingo_card_Diogo.pdf")
        self.assertEqual(calls[1][0][2], "Bingo Card - Diogo")
        self.assertEqual(calls[2][0][1], "bingo_card_3.pdf")
        self.assertEqual(calls[2][0][2], "Bingo Card #3")
        self.assertEqual(calls[3][0][1], "bingo_card_4.pdf")
        self.assertEqual(calls[3][0][2], "Bingo Card #4")
        self.assertEqual(calls[4][0][1], "bingo_card_5.pdf")
        self.assertEqual(calls[4][0][2], "Bingo Card #5")

    @patch('sys.argv', ['bingo_generator.py', '3', '2'])
    @patch('bingo_generator.save_card_as_pdf')
    def test_main_with_participants_containing_spaces(self, mock_save_pdf):
        """Test main function with participant names containing spaces."""
        # Create participants file with names containing spaces
        participants_content = "Aaron Smith\nDiogo Santos\n"
        with open(bingo_generator.PARTICIPANTS_FILE, "w", encoding="utf-8") as f:
            f.write(participants_content)
        
        bingo_generator.main()
        
        # Should call save_card_as_pdf twice
        self.assertEqual(mock_save_pdf.call_count, 2)
        
        # Check that spaces are replaced with underscores in filenames
        calls = mock_save_pdf.call_args_list
        self.assertEqual(calls[0][0][1], "bingo_card_Aaron_Smith.pdf")
        self.assertEqual(calls[0][0][2], "Bingo Card - Aaron Smith")
        self.assertEqual(calls[1][0][1], "bingo_card_Diogo_Santos.pdf")
        self.assertEqual(calls[1][0][2], "Bingo Card - Diogo Santos")

    @patch('sys.argv', ['bingo_generator.py', '25', '1'])
    @patch('sys.exit')
    def test_main_too_many_entries(self, mock_exit):
        """Test main function when requesting more entries than available."""
        with patch('builtins.print') as mock_print:
            bingo_generator.main()
            mock_print.assert_called_with("Error: Not enough entries in the input file.")
            mock_exit.assert_called_with(1)

    @patch('sys.argv', ['bingo_generator.py'])
    @patch('sys.exit')
    def test_main_insufficient_arguments(self, mock_exit):
        """Test main function with insufficient arguments."""
        with patch('builtins.print') as mock_print:
            bingo_generator.main()
            mock_print.assert_called_with("Usage: python bingo_generator.py <entries_per_card> <number_of_cards>")
            mock_exit.assert_called_with(1)

    @patch('sys.argv', ['bingo_generator.py', '5', '2', 'extra'])
    @patch('sys.exit')
    def test_main_too_many_arguments(self, mock_exit):
        """Test main function with too many arguments."""
        with patch('builtins.print') as mock_print:
            bingo_generator.main()
            mock_print.assert_called_with("Usage: python bingo_generator.py <entries_per_card> <number_of_cards>")
            mock_exit.assert_called_with(1)

    @patch('sys.argv', ['bingo_generator.py', '5', '2'])
    @patch('sys.exit')
    def test_main_missing_entries_file(self, mock_exit):
        """Test main function when entries file doesn't exist."""
        # Remove the entries file
        os.remove(self.entries_file)
        
        with patch('builtins.print') as mock_print:
            bingo_generator.main()
            mock_print.assert_called_with("Error: Not enough entries in the input file.")
            mock_exit.assert_called_with(1)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up after tests."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_end_to_end_workflow_without_participants(self):
        """Test the complete workflow from file reading to PDF generation."""
        # Create entries file
        entries = ["Meeting phrase 1", "Meeting phrase 2", "Meeting phrase 3", 
                  "Meeting phrase 4", "Meeting phrase 5", "Meeting phrase 6"]
        entries_file = bingo_generator.ENTRIES_FILE
        
        with open(entries_file, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(f"{entry}\n")
        
        # Read entries
        loaded_entries = bingo_generator.read_lines(entries_file)
        self.assertEqual(loaded_entries, entries)
        
        # Generate cards
        num_entries = 4
        num_cards = 2
        
        for i in range(num_cards):
            card = bingo_card.generate_bingo_card(loaded_entries, num_entries)
            self.assertEqual(len(card), num_entries)
            self.assertTrue(all(entry in loaded_entries for entry in card))

    @patch('sys.argv', ['bingo_generator.py', '9', '2'])
    def test_end_to_end_with_participants(self):
        """Test complete integration with participants file."""
        # Create entries file with enough entries
        entries = [f"Entry {i}" for i in range(1, 21)]
        with open(bingo_generator.ENTRIES_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(entries))
        
        # Create participants file
        with open(bingo_generator.PARTICIPANTS_FILE, "w", encoding="utf-8") as f:
            f.write("Aaron\nDiogo\n")
        
        # Run main function
        bingo_generator.main()
        
        # Check that correct PDF files were created
        self.assertTrue(os.path.exists("bingo_card_Aaron.pdf"))
        self.assertTrue(os.path.exists("bingo_card_Diogo.pdf"))
        
        # Check that generic files were not created
        self.assertFalse(os.path.exists("bingo_card_1.pdf"))
        self.assertFalse(os.path.exists("bingo_card_2.pdf"))

    @patch('sys.argv', ['bingo_generator.py', '9', '2'])
    def test_end_to_end_without_participants(self):
        """Test complete integration without participants file."""
        # Create entries file with enough entries
        entries = [f"Entry {i}" for i in range(1, 21)]
        with open(bingo_generator.ENTRIES_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(entries))
        
        # Run main function (no participants.txt file)
        bingo_generator.main()
        
        # Check that generic PDF files were created
        self.assertTrue(os.path.exists("bingo_card_1.pdf"))
        self.assertTrue(os.path.exists("bingo_card_2.pdf"))

    def test_unicode_entries(self):
        """Test handling of Unicode characters in entries."""
        unicode_entries = [
            "Café meeting ☕",
            "Résumé review 📄", 
            "Naïve approach 🤔",
            "Piñata party 🎉",
            "Emoji support 😀"
        ]
        
        entries_file = "unicode_entries.txt"
        with open(entries_file, "w", encoding="utf-8") as f:
            for entry in unicode_entries:
                f.write(f"{entry}\n")
        
        loaded_entries = bingo_generator.read_lines(entries_file)
        self.assertEqual(loaded_entries, unicode_entries)
        
        # Test card generation with Unicode
        card = bingo_card.generate_bingo_card(loaded_entries, 3)
        self.assertEqual(len(card), 3)
        self.assertTrue(all(entry in unicode_entries for entry in card))

    def test_participants_with_unicode_names(self):
        """Test handling of Unicode characters in participant names."""
        unicode_participants = [
            "José Silva",
            "François Müller",
            "李小明",
            "محمد أحمد"
        ]
        
        participants_file = "unicode_participants.txt"
        with open(participants_file, "w", encoding="utf-8") as f:
            for participant in unicode_participants:
                f.write(f"{participant}\n")
        
        loaded_participants = bingo_generator.read_lines(participants_file)
        self.assertEqual(loaded_participants, unicode_participants)


if __name__ == '__main__':
    unittest.main()
