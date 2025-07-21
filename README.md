# 🎉 Standup Bingo Card Generator

A Python application that generates randomized Bingo cards as PDF files, perfect for making team standups more engaging! The application reads entries from a customizable text file and creates professional-looking PDF bingo cards with your specified content.

## ✨ Features

- 📄 Generate multiple PDF bingo cards with random entries
- 🎲 Customizable number of entries per card
- 📝 Easy-to-edit text file for bingo entries
- 🎨 Clean, professional PDF layout
- 🔀 Random sampling ensures unique cards
- 💻 Simple command-line interface

## 🚀 Quick Start

1. **Clone or download** this repository
2. **Install dependencies**: `pip install reportlab`
3. **Create your entries file**: Copy `bingo_entries.example.txt` to `bingo_entries.txt` and customize
4. **Generate cards**: `python bingo_generator.py 10 6`

## 📦 Requirements

- **Python 3.6+**
- **reportlab** library for PDF generation

### Installation

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

### Entry File Format

- One entry per line
- Empty lines are ignored
- No special formatting required
- Supports UTF-8 encoding for international characters

## 🎯 Use Cases

- **Team Standups**: Make daily standups more engaging
- **Meeting Bingo**: Create cards for common meeting phrases
- **Educational Games**: Generate bingo cards for learning activities
- **Event Activities**: Create custom bingo for conferences or workshops
- **Ice Breakers**: Generate "getting to know you" bingo cards

## 🛠️ Troubleshooting

### Common Issues

**Error: 'bingo_entries.txt' not found**
- Make sure you've created `bingo_entries.txt` from the example file
- Check that the file is in the same directory as `bingo_generator.py`

**Error: Not enough entries in the input file**
- Your `bingo_entries.txt` needs at least as many entries as `entries_per_card`
- Add more entries to your file or reduce the `entries_per_card` parameter

**ModuleNotFoundError: No module named 'reportlab'**
- Install the required dependency: `pip install reportlab`

### Verification

To verify everything is working correctly:

```bash
# Check if Python is installed
python --version

# Check if reportlab is installed
python -c "import reportlab; print('reportlab is installed')"

# Test with example entries
cp bingo_entries.example.txt bingo_entries.txt
python bingo_generator.py 5 2
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
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [ReportLab](https://www.reportlab.com/) for PDF generation
- Inspired by the need to make meetings more fun and engaging

