import os
import shutil

from gencontent import copy_directory_contents, generate_pages_recursive


def main(base_path):
    """
    Entry point of the static site generator.

    Behavior:
        - Deletes the existing 'public' directory if it exists.
        - Copies all static assets from the 'static' directory into 'public'.
        - Recursively generates HTML pages for every markdown file found in
          the 'content' directory using 'template.html'.
        - Writes the generated HTML files into the 'public' directory while
          preserving the content directory structure.
    """
    # if os.path.exists("public"):
    #     shutil.rmtree("public")

    # copy_directory_contents("static", "public")

    # generate_pages_recursive("content", "template.html", "public")
    #
    if os.path.exists("docs"):
        shutil.rmtree("docs")

    copy_directory_contents("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    main(base_path)
