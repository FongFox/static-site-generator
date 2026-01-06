import os
import shutil

from gencontent import copy_directory_contents, generate_pages_recursive


def main(base_path):
    """
    Entry point for the static site generator.

    Args:
        base_path: The base URL path where the site will be served.
            - "/" for local development (root)
            - "/REPO_NAME/" for GitHub Pages under https://USERNAME.github.io/REPO_NAME/

    Behavior:
        - Deletes the existing 'docs' directory if it exists.
        - Copies all static assets from 'static' into 'docs'.
        - Recursively generates HTML pages from the 'content' directory
          using 'template.html'.
        - Rewrites internal href/src attributes to be prefixed with base_path.
        - Writes the generated HTML files into the 'docs' directory while
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
