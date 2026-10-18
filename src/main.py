import os
import shutil

from textnode import *
from htmlnode import *
from blocktype import *

def main():
    print("Copying static files to public directory...")
    copy_directory("static/", "public/")

    print("Generating pages...")
    generate_pages_recursive("content/", "template.html", "public/")

def copy_directory(source, destination):
    print("Copying directory: ", source, " to ", destination)
    if os.path.exists(destination):
        shutil.rmtree(destination)

    if os.path.exists(source):
        print("Entering if")
        os.mkdir(destination)
        for item in os.listdir(source):
            path = os.path.join(source, item)
            print("Processing item: ", item)
            if os.path.isdir(path):
                copy_directory(path, os.path.join(destination, item))
            elif os.path.isfile(path):
                print("Copying item: ", item)
                shutil.copy(path, os.path.join(destination, item))

def generate_page(from_path, template_path, dest_path):
    print("Generating page from: ", from_path, " to ", dest_path)
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    extract_tile = extract_title(markdown) or "Untitled"

    template = template.replace("{{ Title }}", extract_tile)
    template = template.replace("{{ Content }}", html_content)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))

        if os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_path)
        elif os.path.isfile(content_path) and content_path.endswith(".md"):
            generate_page(content_path, template_path, dest_path)

if __name__ == "__main__":
    main()