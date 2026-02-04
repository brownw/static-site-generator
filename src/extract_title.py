import re
import os
from block_markdown import *

def extract_title(markdown):
    match = re.match(r"^#\s(.*)", markdown)
    heading = ""
    if match:
        heading = match.group(1)
    return heading.strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #Print a message like "Generating page from from_path to dest_path using template_path".
    #Read the markdown file at from_path and store the contents in a variable.
    try: 
        from_file = open(from_path)
        source = from_file.read()
        from_file.close() 
        print(f"{source}")
        #Read the template file at template_path and store the contents in a variable.
        template_file = open(template_path)
        template = template_file.read()
        template_file.close()
        
        #Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
        html_node = markdown_to_html_node(source)
        html_text = html_node.to_html()
        #print(f"html_text: {html_node.to_html()}")
        #Use the extract_title function to grab the title of the page.
        title = extract_title(source)
        output_text = template.replace("{{ Title }}", title)
        output_text = output_text.replace("{{ Content }}", html_text)
        #Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
        #Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)
        with open(dest_path, 'w') as f:
            f.write(output_text)
    except FileNotFoundError as e:
        print(f"Sorry, the file does not exist: {e}")
    except PermissionError as e:
        print(f"You do not have permission to read this file. {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
