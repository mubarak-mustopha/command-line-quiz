import json
import re
import pdfplumber

PATTERN = re.compile("\d(.*?)\na[.]\s+(\w+)",re.DOTALL)#1. What is a boy\na. A boy is a boy

with pdfplumber.open("gns106+++.pdf") as gns_pdf:
    german_pqs = gns_pdf.pages[30:]#list of pdf pages starting from 30 coz german question starts here.
    #print(german_pqs[0].extract_text())
    match = PATTERN.search(german_pqs[0].extract_text())
    print(match.group(0))