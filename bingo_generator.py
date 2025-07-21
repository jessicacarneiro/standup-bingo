import sys
import random
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from math import ceil, sqrt


ENTRIES_FILE = "bingo_entries.txt"

def read_entries(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        entries = [line.strip() for line in f if line.strip()]
    return entries

def generate_bingo_card(entries, num_entries):
    return random.sample(entries, num_entries)

def save_card_as_pdf(card_entries, card_index):
    pdf_path = f"bingo_card_{card_index + 1}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 50
    card_title = f"Bingo Card #{card_index + 1}"

    # Determine grid size (e.g., for 25 entries → 5x5 grid)
    num_entries = len(card_entries)
    grid_size = ceil(sqrt(num_entries))  # square-ish grid

    # Grid dimensions
    cell_width = (width - 2 * margin) / grid_size
    cell_height = (height - 2 * margin - 40) / grid_size  # reserve some height for title

    # Draw title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - margin / 2, card_title)

    # Set font for cells
    c.setFont("Helvetica", 10)

    # Draw each cell
    for idx, entry in enumerate(card_entries):
        row = idx // grid_size
        col = idx % grid_size

        x = margin + col * cell_width
        y = height - margin - 40 - row * cell_height

        # Draw rectangle
        c.setStrokeColor(colors.black)
        c.rect(x, y - cell_height, cell_width, cell_height, fill=0)

        # Center text
        text_x = x + cell_width / 2
        text_y = y - cell_height / 2
        c.drawCentredString(text_x, text_y, entry)

    c.save()
    print(f"Saved: {pdf_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python bingo_generator.py <entries_per_card> <number_of_cards>")
        sys.exit(1)

    entries_per_card = int(sys.argv[1])
    number_of_cards = int(sys.argv[2])

    if not Path(ENTRIES_FILE).exists():
        print(f"Error: '{ENTRIES_FILE}' not found.")
        sys.exit(1)

    entries = read_entries(ENTRIES_FILE)

    if entries_per_card > len(entries):
        print("Error: Not enough entries in the input file.")
        sys.exit(1)

    for i in range(number_of_cards):
        card = generate_bingo_card(entries, entries_per_card)
        save_card_as_pdf(card, i)

if __name__ == "__main__":
    main()