import docx

doc = docx.Document("SubbaTaniparti.docx")
for i, p in enumerate(doc.paragraphs):
    print(f"[{i:02d}] {repr(p.text)}")
