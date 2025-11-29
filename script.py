import os
import json
from markdown_pdf import MarkdownPdf, Section

# --- Configuration ---
CONFIG_FILE = "config.json"
OUTPUT_SUBFOLDER_NAME = "pdf_output" # <--- New Subfolder Name

try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: Configuration file '{CONFIG_FILE}' not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{CONFIG_FILE}'.")
    exit()

# The config key is expected to point to a directory/folder
INPUT_DIRECTORY = config.get("input_directory") 

if not INPUT_DIRECTORY:
    print("Error: 'input_directory' missing from config.json.")
    exit()

if not os.path.isdir(INPUT_DIRECTORY):
    print(f"Error: Path '{INPUT_DIRECTORY}' is not a valid directory.")
    exit()

# Define the full path for the output subfolder
OUTPUT_DIRECTORY = os.path.join(INPUT_DIRECTORY, OUTPUT_SUBFOLDER_NAME)

# Create the output directory if it does not exist
try:
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    print(f"📦 Output folder ensured: {OUTPUT_SUBFOLDER_NAME}/")
except Exception as e:
    print(f"Fatal Error: Could not create output directory '{OUTPUT_DIRECTORY}'. Error: {e}")
    exit()

CUSTOM_CSS = """
pre {
    background-color: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    font-size: 0.9em;
}

code {
    font-family: 'Consolas', 'Courier New', monospace;
    color: #333333;
}

p > code {
    background-color: #eee;
    border-radius: 3px;
    padding: 2px 4px;
    color: #c95100;
}
"""

# --- Conversion Logic ---

print(f"🔍 Starting conversion process...")
print(f"Target Source Directory: {INPUT_DIRECTORY}")
print("-" * 30)

markdown_files_found = False

# Iterate over all files in the specified directory
for filename in os.listdir(INPUT_DIRECTORY):
    if filename.endswith(".md"):
        markdown_files_found = True
        
        # Construct full input and output paths
        input_filepath = os.path.join(INPUT_DIRECTORY, filename)
        output_filename = filename.replace(".md", ".pdf")
        
        # Output path now points inside the newly defined OUTPUT_DIRECTORY
        output_filepath = os.path.join(OUTPUT_DIRECTORY, output_filename)
        
        print(f"➡️ Processing: {filename}")
        
        try:
            # Read the markdown content
            with open(input_filepath, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Initialize the MarkdownPdf object and save the PDF
            pdf = MarkdownPdf()
            pdf.add_section(
                Section(markdown_content),
                user_css=CUSTOM_CSS
            )
            pdf.meta["title"] = os.path.splitext(input_filepath)[0]
            pdf.save(output_filepath)

            print(f"✅ Saved to: {OUTPUT_SUBFOLDER_NAME}/{output_filename}")
            
        except Exception as e:
            print(f"❌ Failed to process {filename}. Error: {e}")

print("-" * 30)

if not markdown_files_found:
    print("⚠️ No .md files found in the specified directory.")
else:
    print("🎉 Conversion process complete.")