import click
import questionary
import os
import sys
import platform
from .printing import check_os, get_printers, print_file, PDF_PRINTER, validate_page_range

WELCOME_ART = """
  _____       _       _      _____ _      _____ 
 |  __ \     (_)     | |    / ____| |    |_   _|
 | |__) | __ _ _ __ | |_  | |    | |      | |  
 |  ___/ '__| | '_ \| __| | |    | |      | |  
 | |   | |  | | | | | |_  | |____| |____ _| |_ 
 |_|   |_|  |_|_| |_|\__|  \_____|______|_____|
                                                
   >> Your intuitive, cross-platform printer <<
"""

INSTRUCTIONS = """
[ NAVIGATION ]
 • Use ARROW KEYS (↑/↓) to navigate lists.
 • Press ENTER to select an option.
 • Use BACKSPACE to edit text inputs.
 • Press CTRL+C to cancel at any time.

[ PAGE SELECTION ]
 • '*'   : Print all pages (default)
 • '1-5' : Print a specific range
 • '1,3' : Print specific pages

[ OPTIONS ]
 • Choose between COLOR and BLACK & WHITE.
 • Select SINGLE or DOUBLE-SIDED printing.
 • Pick PAPER SIZE (A4/Letter) and AUTO-SCALE.
"""

DUPLEX_WARNING = """
[!] MANUAL DUPLEX NOTICE [!]
If your printer does not support automatic double-sided printing,
you will need to manually RE-INSERT THE PAPER when prompted
by the printer hardware or system dialog.
"""

@click.command()
@click.argument("file_path", type=click.Path(exists=True))
def cli(file_path):
    """An intuitive, interactive printing CLI."""
    # Display Welcome Art and Instructions
    click.clear()
    click.echo(click.style(WELCOME_ART, fg="cyan", bold=True))
    click.echo(click.style(INSTRUCTIONS, fg="white"))
    click.echo(click.style("-" * 50, fg="bright_black"))
    click.echo(f"  Target File: {click.style(os.path.basename(file_path), fg='green', bold=True)}")
    click.echo(click.style("-" * 50, fg="bright_black"))
    click.echo("")

    check_os()
    
    printers = get_printers()
    if not printers:
        click.secho("No printers found and could not initialize a virtual PDF printer.", fg="red")
        sys.exit(1)

    # Prompt user to select a printer
    printer = questionary.select(
        "Which printer would you like to use?",
        choices=printers,
        style=questionary.Style([
            ('qmark', 'fg:cyan bold'),
            ('question', 'bold'),
            ('answer', 'fg:green bold'),
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan'),
            ('selected', 'fg:green'),
        ])
    ).ask()

    if not printer:
        click.echo("Selection cancelled.")
        return

    # Prompt user for page selection
    page_range = questionary.text(
        "Which pages would you like to print?",
        default="*",
        instruction=" (Options: '*' for all, '1-5' for range, '1,3' for list)",
        validate=validate_page_range
    ).ask()

    if not page_range:
        click.echo("Job cancelled.")
        return

    # Prompt for Color Mode
    color_mode = "Color"
    if printer != PDF_PRINTER:
        color_mode = questionary.select(
            "Select color mode:",
            choices=["Color", "Black & White"]
        ).ask()
        
        if not color_mode:
            click.echo("Job cancelled.")
            return

    # Prompt for Duplex Mode
    duplex_mode = "One-Sided"
    if printer != PDF_PRINTER:
        duplex_mode = questionary.select(
            "Select printing side:",
            choices=["One-Sided", "Double-Sided (Long-Edge)", "Double-Sided (Short-Edge)"]
        ).ask()

        if not duplex_mode:
            click.echo("Job cancelled.")
            return

        if "Double-Sided" in duplex_mode:
            click.echo(click.style(DUPLEX_WARNING, fg="bright_yellow", bold=True))

    # Prompt for Paper Size and Scaling
    paper_size = "A4"
    fit_to_page = False
    if printer != PDF_PRINTER:
        paper_size = questionary.select(
            "Select paper size:",
            choices=["A4", "Letter", "Legal", "A5"]
        ).ask()
        
        if not paper_size:
            click.echo("Job cancelled.")
            return
            
        fit_to_page = questionary.confirm(
            "Fit to page (auto-scale)?",
            default=False
        ).ask()

    output_path = None
    if printer == PDF_PRINTER:
        # Prompt for output file name
        output_path = questionary.text(
            "Enter output PDF file path:",
            default=f"printed_{os.path.basename(file_path)}.pdf",
        ).ask()
        if not output_path:
            click.echo("Job cancelled.")
            return
        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"
        copies = 1
    else:
        # Prompt user for number of copies
        copies = questionary.text(
            "How many copies?",
            default="1",
            validate=lambda val: val.isdigit() and int(val) > 0 or "Please enter a positive integer."
        ).ask()

        if not copies:
            click.echo("Job cancelled.")
            return

    # Final confirmation
    action = f"Save '{os.path.basename(file_path)}' as '{output_path}'" if printer == PDF_PRINTER else f"Print '{os.path.basename(file_path)}' to '{printer}' ({copies} copies)"
    pages_msg = f" (Pages: {page_range})" if page_range != "*" else ""
    color_msg = f" [{color_mode}]" if printer != PDF_PRINTER else ""
    duplex_msg = f" [{duplex_mode}]" if printer != PDF_PRINTER else ""
    layout_msg = f" [{paper_size}, Fit: {fit_to_page}]" if printer != PDF_PRINTER else ""
    
    confirm = questionary.confirm(
        f"{action}{pages_msg}{color_msg}{duplex_msg}{layout_msg}?",
        default=True
    ).ask()

    if confirm:
        # Notes for Windows users
        if platform.system() == "Windows" and printer != PDF_PRINTER:
            click.secho("\nNote: Color, Duplex, Size, and Scaling on Windows depend on your printer's default settings.", fg="yellow")

        success = print_file(file_path, printer, int(copies), page_range, color_mode, duplex_mode, paper_size, fit_to_page, output_path)
        if success:
            msg = f"File successfully saved to '{output_path}'." if printer == PDF_PRINTER else f"Job successfully submitted to '{printer}'."
            click.secho(f"\nSUCCESS: {msg}", fg="green", bold=True)
        else:
            msg = f"Failed to save file to '{output_path}'." if printer == PDF_PRINTER else f"Failed to submit print job to '{printer}'."
            click.secho(f"\nERROR: {msg}", fg="red", bold=True)
    else:
        click.echo("Print job cancelled.")

if __name__ == "__main__":
    cli()
