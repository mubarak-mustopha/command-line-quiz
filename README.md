# GNS106 Quiz Practice Tool

A Python-based tool I built during my 100 level to extract multiple-choice questions from PDFs and practice them through an interactive quiz application. Originally created to prepare for my GNS106 exam.

## Features

### PDF Question Extractor (`generate-json.py`)
- Extracts multiple-choice and fill-in-the-blank questions from PDF files
- Identifies correct answers marked with `+++` in the source PDF
- Outputs structured JSON for easy processing
- Configurable page ranges for selective extraction
- Handles both 4-option multiple choice and single-answer formats

### Interactive Quiz App (`quiz_app.py`)
- Practice with a customizable number of questions
- Supports both multiple-choice and fill-in-the-blank formats
- Immediate feedback after each answer
- Tracks your score and missed questions
- Optional practice session for questions you got wrong
- Flexible answer matching (case-insensitive, whitespace-insensitive)

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install pdfplumber --break-system-packages
```

## Usage

### Extracting Questions from PDF

Basic usage with defaults (starts at page 30, outputs to `gns-test.json`):
```bash
python generate-json.py
```

Specify custom page range and files:
```bash
python generate-json.py --pdf my-exam.pdf --start 1 --end 50 --output questions.json
```

#### Command-line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--pdf` | `-p` | `./gns106+++.pdf` | Path to the PDF file to parse |
| `--start` | `-s` | `30` | Page number to start parsing |
| `--end` | `-e` | None | Page number to end parsing (parses to end if not specified) |
| `--output` | `-o` | `gns-test.json` | Path for the output JSON file |

#### PDF Format Requirements

The PDF should contain questions in this format:

**Multiple-choice:**
```
12. Who introduced the deductive method?
a. Aristotle +++
b. John Locke
c. Francis Bacon
d. René Descartes
```

**Fill-in-the-blank:**
```
15. What is the capital of France?
a. Paris
```

The `+++` marker indicates the correct answer.

### Running the Quiz

With default questions file (`gns-pq.json`):
```bash
python quiz_app.py
```

With a custom questions file:
```bash
python quiz_app.py questions.json
```

#### Quiz Workflow

1. You'll be prompted for how many questions you want to practice
2. Questions are randomly shuffled each time
3. Answer each question (type the letter for multiple-choice, or the full answer for fill-in)
4. Get immediate feedback on your answers
5. See your final score
6. Optionally practice the questions you missed

#### Example Session

```
Loading quiz from: gns-pq.json

How many questions would you like to practice? 5

Starting quiz with 5 questions...

Result to each question shows immediately after you answer it.

Question 1
Who introduced the deductive method?

a. Aristotle
b. John Locke
c. Francis Bacon
d. René Descartes

Type in your answer: a
Correct!

============================================================
Question 2
What is empiricism?

Type in your answer: knowledge from experience
Correct!

============================================================
...

============================================================
FINAL SCORE: 4/5 
============================================================

You missed 1 question(s).
Would you like to practice your missed questions? (yes/no): yes

Starting practice session with 1 question(s)...
```

## Project Structure

```
.
├── generate-json.py      # PDF question extractor
├── quiz_app.py          # Interactive quiz application
├── gns106+++.pdf        # Source PDF (with +++ markers for answers)
├── gns-pq.json          # Extracted questions in JSON format
└── README.md            # This file
```

## JSON Format

The extracted questions are stored in this format:

```json
[
    {
        "question": "Who introduced the deductive method?",
        "options": [
            "a. Aristotle",
            "b. John Locke",
            "c. Francis Bacon",
            "d. René Descartes"
        ],
        "answer": "a. Aristotle +++"
    },
    {
        "question": "What is empiricism?",
        "options": " ",
        "answer": "Knowledge from experience"
    }
]
```

## Tips for Use

1. **Preparing your PDF**: Mark correct answers with `+++` before extraction
2. **Question quality**: The extractor filters out malformed questions automatically
3. **Answer flexibility**: The quiz app ignores case and whitespace in fill-in answers
4. **Practice strategy**: Use the missed questions feature to focus on weak areas
5. **Random practice**: Questions are shuffled each time for varied practice

## Technical Details

### Answer Matching
- **Multiple-choice**: Compares the first character (a, b, c, or d) - case insensitive
- **Fill-in-the-blank**: Removes all whitespace and compares case-insensitively

### Regex Pattern
The extractor uses this pattern to identify questions:
```python
PATTERN = re.compile(r"""
    (\d+[.].*?)           # Question number and text
    \n                    # Newline separator
    ([A-Da-d][.][a-zA-Z+!?. ]+\n?){1,4}  # 1-4 answer options
    """, re.DOTALL | re.VERBOSE)
```

## Limitations

- PDF must follow the specific format (numbered questions with lettered options)
- Correct answers must be marked with `+++` in the source PDF
- Best results with text-based PDFs (not scanned images)
- Questions with unusual formatting may not be extracted correctly
