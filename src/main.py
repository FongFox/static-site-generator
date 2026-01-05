import os
import shutil

from gencontent import copy_directory_contents, generate_page


def main():
    """
    Entry point of the static site generator.

    This function:
      * deletes the existing 'public' directory if it exists
      * copies all static assets from 'static' into 'public'
      * generates 'public/index.html' from 'content/index.md'
        using 'template.html' and the markdown-to-HTML pipeline.
    """
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_directory_contents("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
