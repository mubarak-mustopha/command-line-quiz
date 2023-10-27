import json
import re
import pdfplumber

PATTERN = re.compile("(\d+[.].*?)\n([a-d][.][a-zA-Z+!? ]+\n?)",re.DOTALL)
QUESTION_LIST = []#a list of {"question":abc,"answer":def}

with pdfplumber.open("gns106+++.pdf") as gns_pdf:
    german_pqs = gns_pdf.pages[30:]#list of pdf pages starting from 30 coz german question starts here.
    for page in german_pqs:            
        match = PATTERN.findall(page.extract_text())
        QUESTION_LIST.extend([{"question":m[0],"answer":m[1]} for m in match])

print(f"There're {len(QUESTION_LIST)} questions available.")
print(QUESTION_LIST[:10])        

with open("gns-pq.json", "w") as gns_json:
    json.dump(QUESTION_LIST,gns_json, indent=8, separators=(',\n',': '))
