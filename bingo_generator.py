import sys
import random
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from math import ceil, sqrt


ENTRIES_FILE = "bingo_entries.txt"
PARTICIPANTS_FILE = "participants.txt"

def read_lines(file_path):
    if not Path(file_path).exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def generate_bingo_card(entries, num_entries):
    return random.sample(entries, num_entries)

def save_card_as_pdf(card_entries, filename, card_title):
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

def main():
    if len(sys.argv) != 3:
        print("Usage: python bingo_generator.py <entries_per_card> <number_of_cards>")
        sys.exit(1)

    entries_per_card = int(sys.argv[1])
    number_of_cards = int(sys.argv[2])

    entries = read_lines(ENTRIES_FILE)
    participants = read_lines(PARTICIPANTS_FILE)

    if entries_per_card > len(entries):
        print("Error: Not enough entries in the input file.")
        sys.exit(1)

    for i in range(number_of_cards):
        card = generate_bingo_card(entries, entries_per_card)

        if i < len(participants):
            name = participants[i].replace(" ", "_")
            filename = f"bingo_card_{name}.pdf"
            card_title = f"Bingo Card - {participants[i]}"
        else:
            filename = f"bingo_card_{i + 1}.pdf"
            card_title = f"Bingo Card #{i + 1}"

        save_card_as_pdf(card, filename, card_title)

if __name__ == "__main__":
    main()