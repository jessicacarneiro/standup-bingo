import sys
import random
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    line_height = 20
    x = margin
    y = height - margin

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, f"Bingo Card #{card_index + 1}")
    y -= 30

    c.setFont("Helvetica", 12)
    for i, entry in enumerate(card_entries, 1):
        c.drawString(x, y, f"{i}. {entry}")
        y -= line_height
        if y < margin:
            c.showPage()
            y = height - margin

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