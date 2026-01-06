# Static Site Generator

A Python-based static site generator that converts Markdown files to HTML pages.

## 🌐 Live Demo
[https://FongFox.github.io/static-site-generator/](https://FongFox.github.io/static-site-generator/)

## ✨ Features

- **Markdown to HTML**: Converts `.md` files to fully styled HTML pages
- **Inline Markdown Support**: Bold (`**text**`), italic (`_text_`), code (`` `code` ``), links, and images
- **Block Elements**: Headings, paragraphs, lists (ordered/unordered), code blocks, and blockquotes
- **Recursive Processing**: Automatically processes nested directories
- **Static Assets**: Copies CSS, images, and other assets to output directory
- **GitHub Pages Ready**: Built-in support for deployment to GitHub Pages

## 🚀 Usage

### Local Development
```bash
python main.py
```
This generates the site in the `docs/` folder with base path `/`.

### GitHub Pages Deployment
```bash
python main.py "/static-site-generator/"
```
Adjust the base path to match your repository name.

## 📁 Project Structure

```
├── content/          # Markdown source files
├── static/           # CSS, images, assets
├── template.html     # HTML template
├── docs/             # Generated site (output)
└── main.py           # Entry point
```

## 🛠️ How It Works

1. Reads Markdown files from `content/` directory
2. Parses Markdown syntax (headings, lists, inline formatting)
3. Converts to HTML using `template.html`
4. Copies static assets from `static/` to `docs/`
5. Maintains directory structure in output

## 📝 Supported Markdown

- **Headings**: `#` to `######`
- **Bold**: `**text**`
- **Italic**: `_text_`
- **Code**: `` `code` ``
- **Links**: `[text](url)`
- **Images**: `![alt](url)`
- **Lists**: Ordered (`1.`) and unordered (`-`)
- **Code blocks**: ``` ```code``` ```
- **Blockquotes**: `> quote`

## 📦 Requirements

- Python 3.10+
- No external dependencies (uses only standard library)
