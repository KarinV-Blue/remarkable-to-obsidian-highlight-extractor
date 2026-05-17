# reMarkable Highlights to Obsidian Extractor

A lightweight, zero‑dependency automation pipeline to instantly extract text highlights from reMarkable `.rm` and `.rmdoc` files directly into your Obsidian Inbox vault.

_Note: I am a total amateur and originally built this tool to scratch my own itch and streamline my personal Second Brain workflow. I wanted a fast, lightweight solution that didn't require installing complex third‑party reMarkable libraries. I'm sharing it here in case it helps anyone else!_

----------

## Features

-   **Zero Dependencies:** Runs entirely on standard, built‑in Python libraries. No complex package installations required.
-   **`.rmdoc` Support:** Automatically unpacks and searches packed reMarkable book archives like folders, reading deep internal page files on the fly.
-   **Smart Paragraph Assembly:** Intelligently stitches visual line breaks and fragmented text chunks back into smooth, continuous paragraphs.
-   **Visual Separation:** Places clean horizontal page divider lines (`---`) between multi‑page highlights for clear layout reading.
-   **Easy One‑Click Execution:** Includes a Windows batch script (`.bat`) featuring automatic version control tracking.

----------

## Setup Instructions

**1. Download the Files**

Download `extract_highlights.py` and `run_extractor.bat` and place them on your computer.

----------

**2. Configure Your Python Script**

Open `extract_highlights.py` in any text editor and update the `OUTPUT_VAULT_FOLDER` variable at the top to point to your Obsidian vault path:

    python
    OUTPUT_VAULT_FOLDER = r"C:\Your\Obsidian\Vault\Inbox"
----
**3. Configure Your Batch File**

Open `run_extractor.bat` in any text editor and update the directory variable path at the top to point to where you download your reMarkable files:

    bat
    cd  /d "C:\Your\reMarkable\Download"

---
**4. Run It**

Double‑click `run_extractor.bat`.

The script will instantly sweep your target folder, convert your highlights, display version details, and safely drop the newly formatted Markdown files directly into your Obsidian vault.

---

**How It Works Under the Hood**

Because text strings inside reMarkable v6 files are embedded sequentially in a binary data container alongside coordinate brush strokes and formatting blocks, standard text viewers struggle to display them cleanly.

This script uses a customized regular expression to isolate standard UTF‑8 string sequences directly out of raw file data. It dynamically strips away proprietary structural tags (such as the trailing l! line endings), filters out system noise fragments or layer names, and merges line sentences into proper flows while maintaining clean spacing.

---

**Contributing**

Since I am a beginner, there are bound to be bugs, text formatting anomalies, or untested edge cases.
Please feel free to open an Issue or submit a Pull Request if you'd like to help improve the parsing logic or expand support for other platforms.
