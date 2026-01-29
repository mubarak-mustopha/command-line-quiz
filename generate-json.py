#! /usr/bin/env python3
import argparse
import json
import re
import pdfplumber

# Regex pattern to extract multiple-choice questions from PDF text
# Matches format:
#   12. What is the deductive method?
#   a. First option
#   b. Second option +++
#   c. Third option
#   d. Fourth option
# The +++ marker indicates the correct answer
PATTERN = re.compile(
    r"""
                     (\d+[.].*?) # Question: starts with number and period (e.g., "12. Question text...")
                     \n          # Newline separating question from answer options 
                     ([A-Da-d][.][a-zA-Z+!?. ]+\n?){1,4} # Options: 1-4 lines starting with a-d/A-D followed by period
                     """,
    re.DOTALL | re.VERBOSE,
)


def split_text(pattern, text):
    """
    Split text using the provided regex pattern.

    Args:
        pattern: Compiled regex pattern or pattern string
        text: Text to split

    Returns:
        List of text segments split by the pattern
    """
    return re.split(pattern, text)


def get_q_and_a_dict(match_string):
    """
    Parse a matched question string into structured question data.

    Extracts the question text, answer options, and correct answer from a
    string containing either:
    - A multiple-choice question with 4 options (a-d), or
    - A fill-in-the-blank question with a single answer

    The correct answer in multiple-choice questions is marked with '+++'.

    Args:
        match_string: Raw text containing a question and its options

    Returns:
        dict: Contains 'question', 'options', and 'answer' keys, or
        None: If the format is invalid (e.g., not 1 or 4 options)

    Example:
        Input: "12. Who introduced logic?\na. Aristotle +++\nb. Plato\nc. Socrates\nd. Kant"
        Output: {
            'question': 'Who introduced logic?',
            'options': ['a. Aristotle', 'b. Plato', 'c. Socrates', 'd. Kant'],
            'answer': 'a. Aristotle +++'
        }
    """
    # Split question from options at the first option line (starts with 'a.' or 'A.')
    question, options = split_text("\n(?=[Aa][.])", match_string)

    # Remove question number prefix (e.g "12." or "12. ")
    question = re.sub("^\d+[. ]{1,2}", "", question)

    # Parse options into list
    options = options.strip("\n").split("\n")

    # Handle fill-in-the-blank questions (single answer, no multiple choice)
    if len(options) == 1:
        answer = options[0]

        # Extract just answer text (e.g "Muby" from "a. Muby")
        return {
            "question": question,
            "options": " ",
            "answer": re.sub(r"^[Aa][.] ", "", answer),
        }

    # Validate multiple-choice format (must have exactly 4 options)
    if len(options) != 4:
        return None

    # Find correct answer (marked with '+++')
    answer = [opt for opt in options if opt.endswith("+++")]
    if not answer or len(answer) != 1:
        return None

    # Remove answer marks from options to display
    options = [opt.strip("+++") for opt in options]

    return {"question": question, "options": options, "answer": answer[0]}


def parse_pdf(file_path, pattern=PATTERN, page_start=1, page_end=None, func=None):
    """
    Extract questions from a PDF file using pattern matching.

    Reads through specified pages of a PDF, finds all text matching the pattern,
    and optionally transforms each match using a provided function.

    Args:
        file_path (str): Path to the PDF file to parse
        pattern (re.Pattern, optional): Compiled regex pattern to match questions.
            Defaults to PATTERN (multiple-choice question format)
        page_start (int, optional): First page to parse (1-indexed). Defaults to 1
        page_end (int, optional): Last page to parse (1-indexed). If None, parses
            to the end of the document. Defaults to None
        func (callable, optional): Function to transform each matched string.
            If None, returns raw matched strings. Defaults to None

    Returns:
        list: Matched text from all pages. If func is provided, returns transformed
            results. Otherwise returns raw regex matches

    Example:
        # Parse pages 30-50 and structure the questions
        questions = parse_pdf("exam.pdf", page_start=30, page_end=50,
                            func=get_q_and_a_dict)
    """
    # Collect all matched questions across pages
    matches = []

    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages

        if page_end is None:
            pages_to_parse = pages[page_start - 1 :]
        else:
            pages_to_parse = pages[page_start - 1 : page_end]

        for page in pages_to_parse:
            # Extract text with slight tolerance for character alignment
            page_text = page.extract_text(x_tolerance=1)

            # Find all pattern matches on this page
            page_matches = [match.group() for match in pattern.finditer(page_text)]

            if func:
                page_matches = [func(match) for match in page_matches]

            matches.extend(page_matches)

    return matches


def convert_to_json(data, file_path):
    """
    Save a Python object as a formatted JSON file.

    Writes the data to a JSON file with readable indentation and formatting.

    Args:
        data: Python object to serialize (typically dict or list)
        file_path (str): Path where the JSON file should be saved

    Returns:
        None

    Example:
        questions = [{"question": "What is 2+2?", "answer": "4"}]
        convert_to_json(questions, "output.json")
    """

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        "-s",
        type=int,
        default=30,
        help="Page number to start parsing (default: 30)",
    )
    parser.add_argument(
        "--end",
        "-e",
        type=int,
        default=None,
        help="Page number to stop parsing (default: parse to end of document)",
    )
    parser.add_argument(
        "--pdf",
        "-p",
        type=str,
        default="./gns106+++.pdf",
        help="Path to PDF file to parse (default: ./gns106+++.pdf)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="gns-test.json",
        help="Path to output JSON file (default: gns-test.json)",
    )

    args = parser.parse_args()

    questions = parse_pdf(
        args.pdf, PATTERN, args.start, args.end, func=get_q_and_a_dict
    )

    convert_to_json(questions, args.output)

    print(f"Successfully extracted {len(questions)} questions from {args.pdf}")
    print(f"Output saved to {args.output}")
