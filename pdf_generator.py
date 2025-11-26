"""
PDF generation module for bingo cards.

This module handles all PDF-related functionality including creating
bingo cards with interactive checkboxes in a grid layout.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from math import ceil, sqrt


def save_card_as_pdf(card_entries, filename, card_title):
    """
    Generate a PDF bingo card with interactive checkboxes.
    
    Args:
        card_entries (list): List of entries to include on the bingo card
        filename (str): Output PDF filename
        card_title (str): Title to display on the card
    
    The PDF will have:
    - A grid layout based on the number of entries (e.g., 3x3 for 9 entries)
    - Interactive checkboxes for each entry
    - Entry text next to each checkbox
    - A centered title at the top
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 50

    # Grid layout
    num_entries = len(card_entries)
    grid_size = ceil(sqrt(num_entries))
    cell_width = (width - 2 * margin) / grid_size
    cell_height = (height - 2 * margin - 40) / grid_size

    # Draw title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - margin / 2, card_title)

    c.setFont("Helvetica", 9)
    checkbox_size = 12

    for idx, entry in enumerate(card_entries):
        row = idx // grid_size
        col = idx % grid_size

        x = margin + col * cell_width
        y = height - margin - 40 - row * cell_height

        # Draw cell border
        c.setStrokeColor(colors.black)
        c.rect(x, y - cell_height, cell_width, cell_height, fill=0)

        # Define checkbox position
        checkbox_x = x + 5
        checkbox_y = y - checkbox_size - 5

        # Add editable checkbox using AcroForm
        field_name = f"cb_{idx}"
        c.acroForm.checkbox(
            name=field_name,
            tooltip=entry,
            x=checkbox_x,
            y=checkbox_y,
            size=checkbox_size,
            buttonStyle='check',
            borderColor=colors.black,
            fillColor=colors.white,
            textColor=colors.black,
            forceBorder=True
        )

        # Draw entry text to the right
        text_x = checkbox_x + checkbox_size + 4
        text_y = checkbox_y + 2
        c.drawString(text_x, text_y, entry)

    c.save()
    print(f"Saved: {filename}")
