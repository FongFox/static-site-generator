import os
import shutil

from markdown_blocks import markdown_to_html_node


def copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copies all contents of a source directory to a destination directory.
    This function will DELETE the destination directory if it already exists before
    copying the new content.

    Args:
        source_dir (str): Relative path of the source directory
        dest_dir (str): Relative path of the destination directory

    Returns:
        None

    Raises:
        Exception: If the source directory does not exist

    Processing Logic:
        - Checks if source directory exists; raises Exception if not found
        - Deletes destination directory if it already exists (using shutil.rmtree)
        - Creates a new destination directory
        - Iterates through all items in source directory:
            * If item is a file: copies it directly to destination
            * If item is a directory: creates new directory and recursively
              calls itself to copy contents

    Important Notes:
        - This function will COMPLETELY DELETE the destination directory if it exists
        - Uses recursion to handle nested directory structures
        - May fail if insufficient file/directory access permissions

    Example:
        >>> copy_directory_contents("static", "public")
        # Copies all contents from ./static/ to ./public/
    """

    cwd = os.getcwd()
    src_dir_path = os.path.join(cwd, source_dir)
    dest_dir_path = os.path.join(cwd, dest_dir)

    if not os.path.exists(src_dir_path):
        raise Exception("Folder path not existed!")

    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    os.mkdir(dest_dir_path)

    src_dir = os.listdir(src_dir_path)
    for item in src_dir:
        cur_path = os.path.join(src_dir_path, item)
        if os.path.isfile(cur_path):
            shutil.copy(cur_path, dest_dir_path)
        else:
            new_des_dir_path = os.path.join(dest_dir_path, item)
            os.mkdir(new_des_dir_path)
            copy_directory_contents(cur_path, new_des_dir_path)


def extract_title(markdown: str) -> str:
    """
    Extract the first H1 title from a markdown string.

    The function searches each line of the markdown for a line that starts
    with a single '#' character followed by a space (an H1 heading).
    It returns the text of that heading with leading and trailing
    whitespace removed.

    Args:
        markdown: The full markdown document as a single string.

    Returns:
        The text content of the first H1 heading.

    Raises:
        Exception: If no H1 heading is found in the markdown.
    """
    lines = markdown.split("\n")
    for line in lines:
        temp = line.lstrip()
        if temp.startswith("# "):
            title = temp[2:]
            title = title.strip()
            return title

    raise Exception("No h1 title found in markdown")


def generate_page(from_path, template_path, dest_path):
    """
    Generate a full HTML page from a markdown file and an HTML template.

    This function:
      * reads markdown content from `from_path`
      * reads an HTML template from `template_path`
      * converts the markdown to an HTML string using `markdown_to_html_node().to_html()`
      * extracts the page title from the markdown using `extract_title()`
      * replaces the `{{ Title }}` and `{{ Content }}` placeholders in the template
      * writes the final HTML page to `dest_path`, creating parent directories if needed.

    Args:
        from_path: Path to the source markdown file.
        template_path: Path to the HTML template file.
        dest_path: Path where the generated HTML file should be written.

    Raises:
        Exception: If `extract_title` cannot find an H1 title in the markdown.
        OSError: If there is an error reading or writing files.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    root = markdown_to_html_node(markdown)
    html_content = root.to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_content)

    dir_path = os.path.dirname(dest_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)


if __name__ == "__main__":
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html",
    )
