#!/usr/bin/env python3
"""
Quick test script to verify the checkbox functionality works correctly.
Run this to test specific checkbox features without running the full test suite.
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bingo_generator

def test_checkbox_functionality():
    """Test that checkboxes are properly created in PDFs."""
    print("Testing checkbox functionality...")
    
    with patch('bingo_generator.canvas.Canvas') as mock_canvas_class:
        # Create mock canvas and acroForm
        mock_canvas = MagicMock()
        mock_acroform = MagicMock()
        mock_canvas.acroForm = mock_acroform
        mock_canvas_class.return_value = mock_canvas
        
        # Test data
        entries = ["Test Entry 1", "Test Entry 2", "Test Entry 3"]
        filename = "test_checkbox.pdf"
        title = "Checkbox Test Card"
        
        # Call the function
        bingo_generator.save_card_as_pdf(entries, filename, title)
        
        # Verify checkboxes were created
        assert mock_acroform.checkbox.call_count == len(entries), f"Expected {len(entries)} checkboxes, got {mock_acroform.checkbox.call_count}"
        
        # Verify checkbox parameters
        checkbox_calls = mock_acroform.checkbox.call_args_list
        for i, call in enumerate(checkbox_calls):
            args, kwargs = call
            assert kwargs['name'] == f"cb_{i}", f"Expected checkbox name 'cb_{i}', got '{kwargs['name']}'"
            assert kwargs['tooltip'] == entries[i], f"Expected tooltip '{entries[i]}', got '{kwargs['tooltip']}'"
            assert kwargs['size'] == 12, f"Expected checkbox size 12, got {kwargs['size']}"
            assert kwargs['buttonStyle'] == 'check', f"Expected buttonStyle 'check', got '{kwargs['buttonStyle']}'"
        
        print("✅ Checkbox functionality test passed!")
        
        # Verify grid layout
        expected_grid_size = 2  # ceil(sqrt(3)) = 2
        assert mock_canvas.rect.call_count == len(entries), f"Expected {len(entries)} rectangles, got {mock_canvas.rect.call_count}"
        
        print("✅ Grid layout test passed!")
        
        # Verify text drawing
        assert mock_canvas.drawString.call_count == len(entries), f"Expected {len(entries)} text draws, got {mock_canvas.drawString.call_count}"
        
        print("✅ Text drawing test passed!")

def test_participant_naming():
    """Test that participant names are correctly used in filenames."""
    print("\nTesting participant naming functionality...")
    
    with patch('bingo_generator.save_card_as_pdf') as mock_save:
        with patch('bingo_generator.read_lines') as mock_read:
            with patch('sys.argv', ['bingo_generator.py', '3', '2']):
                # Mock entries and participants
                mock_read.side_effect = [
                    ["Entry 1", "Entry 2", "Entry 3", "Entry 4", "Entry 5"],  # entries
                    ["Aaron Smith", "Diogo Santos"]  # participants
                ]
                
                # Run main function
                bingo_generator.main()
                
                # Verify save_card_as_pdf was called with correct parameters
                assert mock_save.call_count == 2, f"Expected 2 calls, got {mock_save.call_count}"
                
                calls = mock_save.call_args_list
                
                # First call should use Aaron Smith
                first_call_filename = calls[0][0][1]
                first_call_title = calls[0][0][2]
                assert first_call_filename == "bingo_card_Aaron_Smith.pdf", f"Expected 'bingo_card_Aaron_Smith.pdf', got '{first_call_filename}'"
                assert first_call_title == "Bingo Card - Aaron Smith", f"Expected 'Bingo Card - Aaron Smith', got '{first_call_title}'"
                
                # Second call should use Diogo Santos
                second_call_filename = calls[1][0][1]
                second_call_title = calls[1][0][2]
                assert second_call_filename == "bingo_card_Diogo_Santos.pdf", f"Expected 'bingo_card_Diogo_Santos.pdf', got '{second_call_filename}'"
                assert second_call_title == "Bingo Card - Diogo Santos", f"Expected 'Bingo Card - Diogo Santos', got '{second_call_title}'"
                
                print("✅ Participant naming test passed!")

if __name__ == "__main__":
    test_checkbox_functionality()
    test_participant_naming()
    print("\n🎉 All tests passed! The checkbox and participant functionality is working correctly.")
