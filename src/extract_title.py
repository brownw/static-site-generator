import re

def extract_title(markdown):
    match = re.match(r"^#\s(.*)", markdown)
    heading = ""
    if match:
        heading = match.group(1)
    return heading.strip()

