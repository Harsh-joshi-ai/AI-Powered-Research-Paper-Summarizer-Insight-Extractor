import os
import re
import uuid
import uuid
import fitz
import json
from datetime import datetime

# extract text from pdf
def extract_text_from_pdf(pdf_path):
    doc=fitz.open(pdf_path)
    text=""
    for page in doc:
        text+=page.get_text()
    return text

#text cleaning
def clean_text(text):
    text=re.sub(r"\s+", "", text)
    text=re.sub(r"\n+", "\n", text)
    return text.strip()


#extract title
def extract_title(text):
    lines=text.split("\n")
    title=[]
    collect_title=False
    for line in lines[:15]:
        if re.search(r'\b(prepared for|published|submitted)\b', line, re.IGNORECASE):
            continue

        else:
            capturing_title = True

        if capturing_title:
            # Check if line has clear author markers (like "and" or emails)
            if (re.search(r',', line) or
                re.search(r'@', line) or
                re.search(r'\band\b', line) or
                re.search(r'\*?\d+', line, re.IGNORECASE)): 
                break  # This is the author line, so we stop
            else:
                title.append(line)  # Still title

    title = " ".join(title).strip() if title else "Unknown title"
    return title


# extract author


import re
def author_extraction(text, title):
    lines = text.split('\n')
    author_lines = []
    collecting_authors = False
    
    # Loop through each line
    for line in lines:
        # Check if we hit the abstract section
        if re.search(r'\b(Abstract|Abstract:|Abstract-)\b', line, re.IGNORECASE):
            break  # Stop once we reach abstract
        
        # Check if this line is part of the title
        if line.strip() in title:
            collecting_authors = True  # After title, we start collecting authors
        elif collecting_authors:
            author_lines.append(line.strip())

    
    
    return author_lines if author_lines else ["Unknown authors"]




import re

def clean_author_names(author_lines):
    """
    Given raw author lines, extract only the author names as a comma-separated list.
    """
    
    # Patterns that indicate a line should be skipped entirely
    skip_patterns = [
        r'arXiv:\S+',
        r'\b\d{4}\b.*\d{4}',
        r'^\s*\d{1,2}\s+\w',
        r'@',
        r'\b(Department|Division|Office|Center|College|University|Institute|Program|School|Lab)\b',
        r'\b(USA|Maryland|Virginia|Korea|Seoul|Durham|Bethesda|Williamsburg|Silver Spring)\b',
        r'\b(E-mail|Email)\b',
        r'^\s*\d{5}\b',
        r'\bFebruary|January|March|April|May|June|July|August|September|October|November|December\b',
    ]

    all_names = []

    for line in author_lines:
        line = line.strip()
        if not line:
            continue

        # Skip non-author lines
        if any(re.search(p, line, re.IGNORECASE) for p in skip_patterns):
            continue

        # Remove email groups like {name}@domain.com
        line = re.sub(r'\{[^}]*\}@\S+', '', line)

        # Remove standalone emails
        line = re.sub(r'\S+@\S+', '', line)

        # Remove superscript numbers/symbols attached to names e.g. Zhang*1, Hong1,
        line = re.sub(r'[\*†‡§¶#∗]+\d*|\d+[\*†‡§¶#∗]*', '', line)

        # Normalize "and" / "&" as a separator -> comma
        line = re.sub(r'\s+and\s+|\s*&\s*', ', ', line, flags=re.IGNORECASE)

        # Now split on commas to get individual name tokens
        raw_names = line.split(',')

        for name in raw_names:
            name = name.strip(' ,;')
            # Keep only tokens that look like a real name:
            # must have at least 2 words, each starting with a capital letter
            if name and re.match(r'^[A-Z][a-záéíóúàèìòùäëïöüñçA-Z.\-]+(\s+[A-Z][a-záéíóúàèìòùäëïöüñçA-Z.\-]+)+$', name):
                all_names.append(name)

    return ', '.join(all_names) if all_names else "Unknown authors"

#extract abstract


def extract_abstract(text):
    abstract_match = re.search(r'\b(Abstract|Abstract:|Abstract-)\b', text, re.IGNORECASE)
    if not abstract_match:
        return "Abstract Not Found"

    abstract_start = abstract_match.end()
    abstract_content = []

    # Split the text from the abstract start onward into lines
    lines = text[abstract_start:].split('\n')
    for line in lines:
        if re.search(r'\b(introduction|1.introduction|1  Introduction|II. DEFINITIONS|2.related work|Contents|2\nexperimental setup|keywords)\b', line, re.IGNORECASE):
            break  # Stop when we hit introduction
        abstract_content.append(line.strip())

    return '\n'.join(abstract_content) if abstract_content else "Abstract Not Found"


# content extraction
def extract_content(text):
    content_match = re.search(r'\b(Introduction|1\. Introduction|I\. Introduction|II\. DEFINITIONS|2\. Related Work|Contents|2\nExperimental Setup|Keywords)\b', text, re.IGNORECASE)
    if not content_match:
        return "Content Not Found"

    content_start = content_match.end()
    content = text[content_start:].strip()
    return content if content else "Content Not Found"


# json output
def create_json_structure(pdf_path, raw_text):
    cleaned_text = clean_text(raw_text)

    title = extract_title(raw_text)
    authors = author_extraction(raw_text, title)
    authors_name=clean_author_names(authors)
    abstract = extract_abstract(raw_text)
    content = extract_content(raw_text)

    document_id = str(uuid.uuid4())

    paper_json = {
        "document_id": document_id,
        "source_file": os.path.basename(pdf_path),
        "metadata": {
            "title": title,
            "authors": authors_name,
            "publication_year": None,
            "doi": None,
            "keywords": [],
            "created_at": datetime.utcnow().isoformat()
        },
        "abstract": abstract,
        "content": content
    }

    return paper_json


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    pdf_file = "data\\Machine Learning .pdf"
    output_dir = "parsed_output"
    os.makedirs(output_dir, exist_ok=True)

    raw_text = extract_text_from_pdf(pdf_file)

    paper_data = create_json_structure(pdf_file, raw_text)

    output_path = os.path.join(
        output_dir,
        f"{paper_data['document_id']}.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(paper_data, f, indent=4)

    print("✅ JSON Created Successfully!")
    print("Saved at:", output_path)

    



