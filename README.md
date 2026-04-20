# 🖨️ Print CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](#)

**Print CLI** is a modern, intuitive, and cross-platform command-line interface for printing documents. It abstracts away the complexity of native system commands (`lp`, `PowerShell`, `CUPS`) into a beautiful, interactive experience that works seamlessly on **Linux, macOS, and Windows**.

---

## ✨ Key Features

*   **🎨 Interactive UI:** Beautiful, color-coded menus for selecting printers and options.
*   **🖼️ Universal Support:** Print PDFs, Images (`.jpg`, `.png`, `.gif`), and Text (`.txt`, `.md`, `.log`) with automatic PDF conversion.
*   **📦 Batch Printing:** Pass multiple files or entire directories. Automatically discovers all supported files.
*   **🔗 Smart Merging:** Combine multiple files into a single, seamless PDF print job on the fly.
*   **🤖 AI & Automation Ready:** Use command-line flags to skip prompts—perfect for scripts and AI agents.
*   **📄 Advanced Page Control:** Select specific ranges (`1-5`), lists (`1,3,5`), or a mix of both.
*   **🌓 Full Print Control:** Toggle Color/Grayscale, Duplex (one/two-sided), Orientation, and Paper Size (A4, Letter, etc.).
*   **💾 Always-on PDF Support:** A "Save to PDF" option is always available, even if no physical printers are found.

---

## 🚀 Installation

Install the package in editable mode using pip:

```bash
git clone https://github.com/HimanshuKumarSah/print-cli.git
cd print-cli
pip install -e .
```

---

## 📖 Usage

### 🎮 Interactive Mode
Simply pass a file or folder path. The tool will guide you through the rest.

```bash
print-cli document.pdf
```

### 📁 Bulk & Folder Printing
Provide multiple paths or a directory to trigger batch mode.

```bash
print-cli image.png report.pdf ./docs_folder/
```

### 🤖 Automation (Non-Interactive)
Perfect for AI agents or CI/CD scripts. Use flags to skip menus and `-y` to confirm automatically.

```bash
# Print 2 copies in B&W, double-sided, pages 1-3, and skip confirmation
print-cli report.pdf --printer "Office-HP-Laser" --pages 1-3 --bw --sides two-sided-long-edge -n 2 -y
```

---

## 🛠️ Command Line Options

| Flag | Short | Description | Values |
| :--- | :--- | :--- | :--- |
| `--printer` | `-d` | Target printer name | (e.g., "Microsoft Print to PDF") |
| `--pages` | `-p` | Page range selection | `*`, `1-5`, `1,3,5` |
| `--copies` | `-n` | Number of copies | (integer) |
| `--bw` | | Force Black & White | |
| `--color` | | Force Color | |
| `--sides` | | Duplex mode | `one-sided`, `two-sided-long-edge`, `two-sided-short-edge` |
| `--size` | | Paper size | `A4`, `Letter`, `Legal`, `A5` |
| `--orientation`| | Page orientation | `Auto`, `Portrait`, `Landscape` |
| `--fit` | | Auto-scale to page | |
| `--merge` | `-m` | Merge multiple files | |
| `--yes` | `-y` | Skip confirmation | |
| `--output` | `-o` | Save as PDF path | (e.g., "my_scan.pdf") |

---

## 🧭 Page Selection Syntax

When prompted (or using `-p`), you can use the following syntax:
*   `*` : Print all pages (default).
*   `1-5` : Print a continuous range.
*   `1,3,5` : Print specific individual pages.
*   `1-3,5,10-` : A mix (page 10 to end).

---

## 📜 Future Roadmap

- [ ] Printer status indicators (Ink levels, paper status).
- [ ] N-Up printing (multiple pages per sheet).
- [ ] Custom Watermarking (e.g., "DRAFT", "CONFIDENTIAL").
- [ ] Cloud printing integration.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
