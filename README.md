# 🎉 Standup Bingo Card Generator

A Python application that generates randomized Bingo cards as PDF files, perfect for making team standups more engaging! The application reads entries from a customizable text file and creates professional-looking PDF bingo cards with your specified content.

## ✨ Features

- 📄 Generate multiple PDF bingo cards with random entries
- 🎲 Customizable number of entries per card
- 📝 Easy-to-edit text file for bingo entries
- 👥 **Personalized cards** with participant names (optional)
- ☑️ **Interactive checkboxes** for marking off entries
- 🎨 Clean, professional PDF layout with grid design
- 🔀 Random sampling ensures unique cards
- 💻 Simple command-line interface

## 🚀 Quick Start

1. **Clone or download** this repository
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Create your entries file**: Copy `bingo_entries.example.txt` to `bingo_entries.txt` and customize
4. **[Optional] Create participants file**: Create `participants.txt` with participant names (one per line)
5. **Generate cards**: `python bingo_generator.py 10 6`

## 📦 Requirements

- **Python 3.6+**
- **reportlab** library for PDF generation

### Installation

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install reportlab
```

## 📋 Usage

### Basic Command

```bash
python bingo_generator.py <entries_per_card> <number_of_cards>
```

### Parameters

- `entries_per_card`: Number of entries to include on each bingo card
- `number_of_cards`: Number of different bingo cards to generate

### Examples

```bash
# Generate 6 cards with 10 entries each
python bingo_generator.py 10 6

# Generate 3 cards with 15 entries each
python bingo_generator.py 15 3

# Generate 1 card with 20 entries
python bingo_generator.py 20 1
```

## 📁 Project Structure

```
standup-bingo/
├── bingo_generator.py          # Main application script
├── bingo_entries.example.txt   # Example entries file
├── bingo_entries.txt          # Your custom entries (create from example)
├── participants.txt           # Optional: participant names (one per line)
├── requirements.txt           # Python dependencies
├── tests/                     # Test suite
│   └── test_bingo_generator.py
├── README.md                  # This file
├── .gitignore                # Git ignore rules
└── bingo_card_*.pdf          # Generated PDF files (ignored by git)
```

## ⚙️ Configuration

### Setting Up Your Entries

1. Copy the example file:
   ```bash
   cp bingo_entries.example.txt bingo_entries.txt
   ```

2. Edit `bingo_entries.txt` with your custom entries:
   ```
   "Actually, I think..."
   "Can you hear me?"
   "Sorry, I was on mute"
   "Let's take this offline"
   "Circle back"
   # Add as many entries as you want!
   ```

### Setting Up Participants (Optional)

To generate personalized bingo cards with participant names:

1. Create a `participants.txt` file:
   ```bash
   touch participants.txt
   ```

2. Add participant names (one per line):
   ```
   Aaron
   Diogo
   Germano
   Jessica
   Priscilla
   Vinicius
   ```

3. When you generate cards, the first N cards will be named after participants:
   - `bingo_card_Aaron.pdf` with title "Bingo Card - Aaron"
   - `bingo_card_Diogo.pdf` with title "Bingo Card - Diogo"
   - etc.

4. If you request more cards than participants, the extra cards use generic names:
   - `bingo_card_7.pdf` with title "Bingo Card #7"

**Note:** Participant names with spaces are converted to underscores in filenames (e.g., "John Doe" becomes `bingo_card_John_Doe.pdf`).

### File Formats

**Entry File Format:**
- One entry per line
- Empty lines are ignored
- No special formatting required
- Supports UTF-8 encoding for international characters

**Participants File Format:**
- One participant name per line
- Empty lines are ignored
- Supports UTF-8 encoding for international names
- Spaces in names are allowed (converted to underscores in filenames)

## 🎯 Use Cases

- **Team Standups**: Make daily standups more engaging with personalized cards
- **Meeting Bingo**: Create cards for common meeting phrases with team member names
- **Educational Games**: Generate bingo cards for learning activities
- **Event Activities**: Create custom bingo for conferences or workshops with attendee names
- **Ice Breakers**: Generate "getting to know you" bingo cards for team events
- **Remote Teams**: Add personal touch to virtual meetings with named cards

## 🛠️ Troubleshooting

### Common Issues

**Error: 'bingo_entries.txt' not found**
- Make sure you've created `bingo_entries.txt` from the example file
- Check that the file is in the same directory as `bingo_generator.py`

**Error: Not enough entries in the input file**
- Your `bingo_entries.txt` needs at least as many entries as `entries_per_card`
- Add more entries to your file or reduce the `entries_per_card` parameter

**ModuleNotFoundError: No module named 'reportlab'**
- Install the required dependency: `pip install -r requirements.txt`

**Participants file not working**
- Make sure `participants.txt` is in the same directory as `bingo_generator.py`
- Check that participant names are on separate lines
- The participants file is optional - cards will use generic names if it doesn't exist

**PDF checkboxes not working**
- Interactive checkboxes require a PDF viewer that supports forms (Adobe Reader, etc.)
- Some web browsers may not display interactive elements properly

### Verification

To verify everything is working correctly:

```bash
# Check if Python is installed
python --version

# Check if reportlab is installed
python -c "import reportlab; print('reportlab is installed')"

# Test with example entries (basic cards)
cp bingo_entries.example.txt bingo_entries.txt
python bingo_generator.py 5 2

# Test with participants (personalized cards)
echo -e "Alice\nBob\nCharlie" > participants.txt
python bingo_generator.py 9 3
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs or issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🎨 Enhance the PDF layout
- ⚡ Add new output formats

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Run tests: `python -m unittest tests.test_bingo_generator -v`
6. Test thoroughly
7. Submit a pull request

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [ReportLab](https://www.reportlab.com/) for PDF generation
- Inspired by the need to make meetings more fun and engaging

