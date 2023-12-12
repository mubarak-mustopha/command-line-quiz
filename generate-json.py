import json
import re
import pdfplumber

PATTERN = re.compile(r"""
                     (\d+[.].*?)  
                     \n
                     ([A-Da-d][.][a-zA-Z+!?. ]+\n?){1,4}
                     """,re.DOTALL|re.VERBOSE)

def split_text(pattern, text):
    """
    Wrapper function for re.split
    """
    return re.split(pattern,text)
    
def get_q_and_a_dict(match_string):
    """
    Match_string --> multiple choice/german question with options[1/4] 
    returns {question, option, answer}
    """
    # split on the newline followed by a. or A. which is the first option
    question, options = split_text("\n(?=[Aa][.])", match_string)

    #strip out question number
    question = re.sub("^\d+[. ]{1,2}","",question)

    #gotta strip newline before splitting on it, else we get empty string in list
    options = options.strip("\n").split("\n")
    if len(options) == 1:
        answer = options[0]

        #regex return "Muby" from "a. Muby"| "A. Muby"
        return {
            "question":question,
            "options": " ",
            "answer": re.sub("^[Aa][.] ","", answer)}
    
    if len(options) != 4:
        return None
    
    answer = [opt for opt in options if opt.endswith("+++")]
    if not answer or len(answer) != 1:
        return None

    #obscure answer
    options = [opt.strip("+++") for opt in options]

    return {
        "question":question,
        "options": options,
        "answer": answer[0]
    } 


def parse_pdf(file_path ,pattern = PATTERN,page_start = 0, page_end = None  ,func = None):
    """file_path: pdf-file path

        pattern: text search pattern for pdf pages

        page_start: page number to start search

        page_end: page number to end search

        func: function to transform all matched text in each page

        Returns a list of all matched text in every page
    """

    #a list of {"question":abc,"optoin":[]|" ","answer":def}
    MATCH_LIST = []

    with pdfplumber.open(file_path) as gns_pdf:
        pages = gns_pdf.pages
        pages_to_parse = pages[page_start:] if not page_end else pages[page_start:page_end]

        for page in pages_to_parse:
            page_text = page.extract_text(x_tolerance = 1)
            page_match_list = [match.group() 
                                        for match in pattern.finditer(page_text)]
            
            if not func:
                MATCH_LIST.extend(page_match_list)
            else:      
                transformed_match_list = [func(match) for match in page_match_list]
                MATCH_LIST.extend(transformed_match_list)

    print(f"There're {len(MATCH_LIST)} questions available.")
    print(MATCH_LIST[:10])     
    return MATCH_LIST


def convert_to_json(object, file_path):
    """Turns a python object to a json file"""

    with open(file_path, "w") as json_file:
        json.dump(object, json_file , indent=8 , separators=(',\n',': '))


convert_to_json(parse_pdf("gns106+++.pdf", PATTERN,page_start=30 ,func = get_q_and_a_dict),
                 "gns-test.json")
