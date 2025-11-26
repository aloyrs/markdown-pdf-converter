import os
from markdown_pdf import MarkdownPdf, Section

# --- Configuration ---
# Set the input and output filenames
INPUT_FILENAME = "D:/src/loy/python/markdown-pdf-converter/past-year-answer.md"
OUTPUT_FILENAME = "D:/src/loy/python/markdown-pdf-converter/past-year-answer.pdf"

# Custom CSS for styling, specifically targeting code blocks.
# This CSS attempts to mimic a common dark-on-light theme for code blocks.
# You can adjust these values to your preferred style.
CUSTOM_CSS = """
/* General styles for code blocks */
pre {
    background-color: #f6f8fa; /* Light grey background for the block */
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto; /* Ensures long lines can be scrolled */
    font-size: 0.9em;
}

/* Styles for the code itself */
code {
    font-family: 'Consolas', 'Courier New', monospace;
    color: #333333; /* Darker text color */
}

/* Inline code style */
p > code {
    background-color: #eee;
    border-radius: 3px;
    padding: 2px 4px;
    color: #c95100; /* Example color for inline code */
}
"""

# --- Conversion Logic ---

# Check if the input file exists
if not os.path.exists(INPUT_FILENAME):
    print(f"Error: Input file '{INPUT_FILENAME}' not found in the current directory.")
else:
    # Read the markdown content
    with open(INPUT_FILENAME, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Initialize the MarkdownPdf object
    pdf = MarkdownPdf()

    # Add the section with custom CSS applied
    pdf.add_section(
        Section(markdown_content),
        user_css=CUSTOM_CSS
    )
    
    # Optional: Set PDF metadata
    pdf.meta["title"] = os.path.splitext(INPUT_FILENAME)[0]
    
    # Save the PDF file
    pdf.save(OUTPUT_FILENAME)

    print(f"✅ Successfully converted '{INPUT_FILENAME}' to '{OUTPUT_FILENAME}' with custom code block styles.")