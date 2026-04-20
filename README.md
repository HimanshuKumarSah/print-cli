# Print CLI

An intuitive, interactive command-line interface for printing documents on Linux, macOS, and Windows.

## Features
- **Interactive Selection:** Choose from available printers using arrow keys.
- **Universal File Support:** Print PDFs, Images (`.jpg`, `.png`, `.bmp`, `.gif`), and Text files (`.txt`, `.md`, `.log`) with automatic conversion.
- **Bulk & Batch Printing:** Pass multiple files or entire directories. Automatically discovers all supported files.
- **Smart Merging:** Option to merge multiple files into a single seamless print job or print them individually.
- **Automation Ready:** Supports command-line flags to skip interactive prompts—perfect for scripts and AI agents.
- **Page Selection:** Select all pages (`*`), specific ranges (`1-5`), or a list of pages (`1,3,5`).
- **Color Mode:** Choose between Color and Black & White printing.
- **Duplex Support:** Print single-sided or double-sided (Long-edge or Short-edge).
- **Orientation Override:** Force Portrait, Landscape, or use Auto-detection.
- **Layout Control:** Select from popular paper sizes (A4, Letter, Legal, A5) and toggle "Fit to Page" scaling.
- **Always-on PDF Support:** "Print to PDF" is always available to save documents as files.
- **Cross-Platform:** Works seamlessly on Linux, macOS, and Windows.

## Installation
1. Clone the repository.
2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage
Run the `print-cli` command followed by one or more files or directories:
```bash
# Interactive Mode
print-cli document.pdf

# Automation Mode (Skip Prompts)
print-cli document.pdf --printer "My-Printer" --pages "1-5" --bw -y

# Bulk Printing
print-cli image.png report.pdf ./my_documents/
```

### Automation Flags
Pass these flags to skip interactive prompts or for use in scripts/AI agents:
| Flag | Short | Description | Options |
| :--- | :--- | :--- | :--- |
| `--printer` | `-d` | Target printer name | (e.g., "HP-LaserJet") |
| `--pages` | `-p` | Page range selection | `*`, `1-5`, `1,3` |
| `--copies` | `-n` | Number of copies | (integer) |
| `--bw` | | Print in Black & White | |
| `--color` | | Print in Color | |
| `--sides` | | Duplex mode | `one-sided`, `two-sided-long-edge`, `two-sided-short-edge` |
| `--size` | | Paper size | `A4`, `Letter`, `Legal`, `A5` |
| `--orientation`| | Page orientation | `Auto`, `Portrait`, `Landscape` |
| `--fit` / `--no-fit`| | Toggle auto-scaling | |
| `--merge` / `--no-merge`| `-m` / `-nm` | Toggle batch merging | |
| `--yes` | `-y` | Skip confirmation | |
| `--output` | `-o` | Save to PDF path | (e.g., "output.pdf") |

### Workflow
The tool will guide you through:
1. **File Discovery:** Summary of all supported files found.
2. **Printer Selection:** Choose your target device (skipped if `--printer` provided).
3. **Batch Handling:** Choose to merge multiple files (skipped if `--merge` provided).
4. **Page Range:** Specify which pages to include (skipped if `--pages` provided).
5. **Options:** Color, Sides, Orientation, and Media selection (skipped if flags provided).
6. **Copies:** Enter the number of copies (skipped if `--copies` provided).
7. **Confirmation:** Final job review (skipped if `--yes` provided).

### Page Selection Syntax
When prompted for pages, you can use:
- `*`: All pages (default).
- `1-5`: A range of pages.
- `1,3,5`: A specific list of pages.
- `1-3,5,7-9`: A mix of ranges and lists.

## Future Plans
- Printer status indicators (e.g., ink levels, paper jams).
- N-Up printing (multiple pages per sheet).
- Watermarking (e.g., "DRAFT", "CONFIDENTIAL").
