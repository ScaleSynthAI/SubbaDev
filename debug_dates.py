import docx
import re

doc = docx.Document("SubbaTaniparti.docx")
date_regex = re.compile(
    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|June|Jan\.|Feb\.|Mar\.|Apr\.|Jun\.|Jul\.|Aug\.|Sep\.|Oct\.|Nov\.|Dec\.)\s*\d{4}\s*[-–—]\s*(Present|\d{4}|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|June|Jan\.|Feb\.|Mar\.|Apr\.|Jun\.|Jul\.|Aug\.|Sep\.|Oct\.|Nov\.|Dec\.)\s*\d{4})',
    re.IGNORECASE
)

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    if date_regex.search(text) and ("," in text):
        parts = re.split(r'\t+|\s{3,}', text)
        print(f"[{i}] {repr(text)}")
        print(f"  parts: {parts}")
        if len(parts) > 1:
            dates = parts[1].strip()
            print(f"  dates: {repr(dates)}")
            date_parts = re.split(r'[-–—]', dates)
            print(f"  date_parts: {date_parts}")
