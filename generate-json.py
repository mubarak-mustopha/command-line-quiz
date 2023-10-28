import json
import re
import pdfplumber

def get_match_string(fullstring,match):
    """
    A function that takes a string and a regex match object,
    then return the matched substring from the string
    """
    return fullstring[match.start(): match.end()]

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
    question, options = split_text("\n(?=a[.])", match_string)# split on the newline followed by a. which is the first option
    options = options.strip("\n").split("\n")#gotta strip newline before splitting on it, else we get empty string in list
    if len(options) == 1:
        answer = options[0]
        return {"question":question,"options": " ","answer": re.sub("^a[.] ","", answer)}#regex return "Muby" from "a. Muby"
    if len(options) != 4:
        return None
    
    answer = [opt for opt in options if opt.endswith("+++")]
    if not answer or len(answer) != 1:
        return None
    options = [opt.strip("+++") for opt in options]#obscure answer
    return {"question":question,"options": options,"answer": answer[0]} 


PATTERN = re.compile("(\d+[.].*?)\n([a-d][.][a-zA-Z+!?. ]+\n?){1,4}",re.DOTALL)
QUESTION_LIST = []#a list of {"question":abc,"answer":def}

with pdfplumber.open("gns106+++.pdf") as gns_pdf:
    pages = gns_pdf.pages[30:]#list of pdf pages starting from 30 coz german question starts here.
    for page in pages:
        page_text = page.extract_text()
        question_match_list = [get_match_string(page_text,match) for match in PATTERN.finditer(page_text)]
        q_and_a_dict = [get_q_and_a_dict(match) for match in question_match_list]
        QUESTION_LIST.extend(q_and_a_dict)

print(f"There're {len(QUESTION_LIST)} questions available.")
print(QUESTION_LIST[:10])        

with open("gns-pq.json", "w") as gns_json:
    json.dump(QUESTION_LIST,gns_json, indent=8, separators=(',\n',': '))
