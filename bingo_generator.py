import sys
from pathlib import Path
from pdf_generator import save_card_as_pdf
from bingo_card import generate_bingo_card


ENTRIES_FILE = "bingo_entries.txt"
PARTICIPANTS_FILE = "participants.txt"


def read_lines(file_path):
    """
    Read lines from a file, filtering out empty lines.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        list: List of non-empty lines from the file
    """
    if not Path(file_path).exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except (PermissionError, OSError):
        return []


def main():
    """
    Main function to generate bingo cards.
    
    Reads entries from ENTRIES_FILE and optionally participant names from
    PARTICIPANTS_FILE, then generates the specified number of bingo cards.
    """
    if len(sys.argv) != 3:
        print("Usage: python bingo_generator.py <entries_per_card> <number_of_cards>")
        sys.exit(1)
        return  # For testing when sys.exit is mocked

    try:
        entries_per_card = int(sys.argv[1])
        number_of_cards = int(sys.argv[2])
    except (ValueError, IndexError):
        print("Error: entries_per_card and number_of_cards must be integers.")
        sys.exit(1)
        return  # For testing when sys.exit is mocked

    entries = read_lines(ENTRIES_FILE)
    participants = read_lines(PARTICIPANTS_FILE)

    if len(entries) == 0 or entries_per_card > len(entries):
        print("Error: Not enough entries in the input file.")
        sys.exit(1)
        return  # For testing when sys.exit is mocked

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