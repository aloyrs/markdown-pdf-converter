import os
import json
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

def convert_folder_md_to_pdf(config_path: str = "config.json"):
    """
    Converts all .md files in an input folder to .pdf files in a new 
    'output' subfolder within the input directory.
    """
    
    try:
        # 1. Load configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        input_folder = Path(config.get("input_dir"))
        
        if not input_folder:
            print("❌ Error: 'input_dir' missing in config.json.")
            return

    except FileNotFoundError:
        print(f"❌ Error: Config file not found at {config_path}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in {config_path}")
        return
    except Exception as e:
        print(f"❌ An unexpected error occurred during configuration: {e}")
        return

    # 2. Define and create the output directory
    # --- THIS IS THE CHANGE ---
    output_folder = input_folder / "output"
    # --------------------------
    
    output_folder.mkdir(parents=True, exist_ok=True)

    print(f"Starting conversion from '{input_folder}'...")
    print(f"PDFs will be saved to the new subfolder: '{output_folder}'")

    # 3. Process all Markdown files in the input folder
    md_files = list(input_folder.glob("*.md"))
    
    if not md_files:
        print(f"⚠️ Warning: No .md files found directly in '{input_folder}'.")
        return

    for md_file_path in md_files:
        try:
            # Determine output PDF path
            pdf_file_name = md_file_path.stem + ".pdf"
            pdf_file_path = output_folder / pdf_file_name

            print(f"   Converting {md_file_path.name}...")

            # Read the markdown content
            with open(md_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Create a MarkdownPdf instance
            pdf = MarkdownPdf()
            pdf.add_section(Section(markdown_content)) 

            # Save the PDF
            pdf.save(pdf_file_path)
            
            print(f"   ✅ Saved to {pdf_file_path.name}")

        except Exception as e:
            print(f"   ❌ Failed to convert {md_file_path.name}. Error: {e}")

    print("\nConversion process finished.")

if __name__ == "__main__":
    convert_folder_md_to_pdf()