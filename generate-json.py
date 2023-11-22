import json
import re
import pdfplumber

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
    # split on the newline followed by a. which is the first option
    question, options = split_text("\n(?=a[.])", match_string)

    #strip out question number
    question = re.sub("^\d+[. ]{1,2}","",question)

    #gotta strip newline before splitting on it, else we get empty string in list
    options = options.strip("\n").split("\n")
    if len(options) == 1:
        answer = options[0]

        #regex return "Muby" from "a. Muby"
        return {
            "question":question,
            "options": " ",
            "answer": re.sub("^a[.] ","", answer)}
    
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


PATTERN = re.compile(r"""
                     (\d+[.].*?)  
                     \n
                     ([a-d][.][a-zA-Z+!?. ]+\n?){1,4}
                     """,re.DOTALL|re.VERBOSE)

#a list of {"question":abc,"optoin":[]|" ","answer":def}
QUESTION_LIST = []

with pdfplumber.open("gns106+++.pdf") as gns_pdf:
    #list of pdf pages starting from 30 coz non-tabular questions start here.
    pages = gns_pdf.pages[30:]

    for page in pages:
        page_text = page.extract_text(x_tolerance = 1)
        question_match_list = [match.group() 
                                    for match in PATTERN.finditer(page_text)]
        q_and_a_dict = [get_q_and_a_dict(match) for match in question_match_list]
        QUESTION_LIST.extend(q_and_a_dict)

print(f"There're {len(QUESTION_LIST)} questions available.")
print(QUESTION_LIST[:10])     

with open("gns-pq.json", "w") as gns_json:
    json.dump(QUESTION_LIST,gns_json, indent=8, separators=(',\n',': '))
