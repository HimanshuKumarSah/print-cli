# Print CLI

An intuitive, interactive command-line interface for printing documents on Linux, macOS, and Windows.

## Features
- **Interactive Selection:** Choose from available printers using arrow keys.
- **Page Selection:** Select all pages (`*`), specific ranges (`1-5`), or a list of pages (`1,3,5`).
- **Color Mode:** Choose between Color and Black & White printing.
- **Duplex Support:** Print single-sided or double-sided (Long-edge or Short-edge).
- **Orientation Override:** Force Portrait, Landscape, or use Auto-detection.
- **Layout Control:** Select from popular paper sizes (A4, Letter, Legal, A5) and toggle "Fit to Page" scaling.
- **Always-on PDF Support:** "Print to PDF" is always available to save documents as files.
- **Cross-Platform:** Works seamlessly on Linux, macOS, and Windows.
- **Smart Windows Printing:** Uses Microsoft Edge under the hood for precise page selection and orientation on Windows.

## Installation
1. Clone the repository.
2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage
Run the `print-cli` command followed by the path to the file you want to print:
```bash
print-cli document.pdf
```

### Workflow
The tool will guide you through:
1. **Printer Selection:** Choose your target device.
2. **Page Range:** Specify which pages to include.
3. **Color Mode:** Select color or grayscale output.
4. **Sides:** Choose single or double-sided printing (with manual duplex warnings).
5. **Orientation:** Choose between Auto, Portrait, or Landscape.
6. **Media:** Select paper size and toggle auto-scaling.
7. **Copies:** Enter the number of copies (for physical printers).
8. **Confirmation:** Review your job summary before submitting.

### Page Selection Syntax
When prompted for pages, you can use:
- `*`: All pages (default).
- `1-5`: A range of pages.
- `1,3,5`: A specific list of pages.
- `1-3,5,7-9`: A mix of ranges and lists.

## Future Plans
- Printer status indicators (e.g., ink levels, paper jams).
- Support for printing non-PDF files (images, text, Word) via automatic conversion.
- N-Up printing (multiple pages per sheet).
