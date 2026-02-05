import os
import sys
import shutil

from copystatic import copy_files_recursive
from extract_title import *

dir_path_static = "./static"
dir_path_public = "./docs"

def main():
    base_path = sys.argv[1]

    print(base_path)

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive("content/", "template.html", dir_path_public, base_path)

if __name__ == "__main__":
    main()