import os
import re
import zipfile

# =========================================================================
# CONFIGURATION SETTINGS (Edit these to change your folder paths)
# =========================================================================
# The folder where your newly created Markdown files will be saved
OUTPUT_VAULT_FOLDER = r"C:\Your\Obsidian\Vault\Inbox"

# The folder where the script will search for .rm and .rmdoc files
# Set to None to automatically use the folder where this script is located
INPUT_SOURCE_FOLDER = None  

# --- SCRIPT VERSION CONTROL ---
__version__ = "1.0.0"
# =========================================================================


def process_rm_content(binary_content):
    """Cleans and extracts readable text blocks from raw .rm binary bytes."""
    readable_strings = re.findall(rb'[a-zA-Z0-9\s\.,\?!\'":#@\(\)-]{4,}', binary_content)
    
    cleaned_chunks = []
    for s in readable_strings:
        decoded = s.decode('utf-8', errors='ignore').strip()
        
        if decoded.endswith('l!'):
            decoded = decoded[:-2].strip()
            
        if len(decoded) > 5 and decoded != "Layer 1" and "reMarkable" not in decoded:
            cleaned_chunks.append(decoded)
            
    markdown_text = ""
    for i, chunk in enumerate(cleaned_chunks):
        if chunk.endswith('?') or not chunk.endswith(('.', '!', '"', ' ')):
            if i + 1 < len(cleaned_chunks) and cleaned_chunks[i+1][0].islower():
                markdown_text += chunk + " "
            else:
                markdown_text += chunk + "\n\n"
        else:
            markdown_text += chunk + " "
            
    return markdown_text.strip()


def clean_and_convert_folder():
    # Use the configured input path, or fall back to the current directory
    current_folder = INPUT_SOURCE_FOLDER if INPUT_SOURCE_FOLDER else os.getcwd()
    output_folder = OUTPUT_VAULT_FOLDER
    
    print(f"=========================================")
    print(f" reMarkable Extractor Engine Pipeline     ")
    print(f" Script Version: v{__version__}          ")
    print(f"=========================================\n")
    print(f"Scanning folder for .rm and .rmdoc files: {current_folder}")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    else:
        print(f"Saving Markdown files to: {output_folder}\n")
    
    file_count = 0
    
    for file_name in os.listdir(current_folder):
        if file_name.lower().endswith('.rm'):
            file_count += 1
            md_file_name = os.path.splitext(file_name)[0] + ".md"
            md_file_path = os.path.join(output_folder, md_file_name)
            print(f"Processing standard file: {file_name} -> {md_file_name}")
            
            with open(os.path.join(current_folder, file_name), 'rb') as f:
                content = f.read()
                
            text = process_rm_content(content)
            
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write("# Highlights\n\n---\n\n" + text + "\n")

        elif file_name.lower().endswith('.rmdoc'):
            file_count += 1
            md_file_name = os.path.splitext(file_name)[0] + ".md"
            md_file_path = os.path.join(output_folder, md_file_name)
            print(f"Processing packed rmdoc: {file_name} -> {md_file_name}")
            
            rmdoc_path = os.path.join(current_folder, file_name)
            page_contents = []
            
            try:
                with zipfile.ZipFile(rmdoc_path, 'r') as archive:
                    for internal_file in archive.namelist():
                        if internal_file.lower().endswith('.rm'):
                            with archive.open(internal_file) as f:
                                rmdoc_binary = f.read()
                            
                            page_text = process_rm_content(rmdoc_binary)
                            if page_text:
                                page_contents.append(page_text)
                                
                if page_contents:
                    full_extracted_text = "\n\n---\n\n".join(page_contents)
                    with open(md_file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(f"# Highlights from {os.path.splitext(file_name)[0]}\n\n---\n\n" + full_extracted_text + "\n")
                else:
                    print(f"  (Note: No text content found inside {file_name})")
                    
            except zipfile.BadZipFile:
                print(f"  Error: Could not read {file_name}. The file might be corrupted.")
                
    if file_count == 0:
        print("No .rm or .rmdoc files found in the current folder.")
    else:
        print(f"\nSuccess! Processed {file_count} total file(s).")
        print(f"Check your Obsidian Inbox at '{output_folder}' for your text!")


if __name__ == "__main__":
    clean_and_convert_folder()