import click
import questionary
import os
import sys
import platform
import tempfile
from .printing import check_os, get_printers, print_file, PDF_PRINTER, validate_page_range
from .converter import convert_to_pdf, collect_files, merge_pdfs

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

[ AUTOMATION ]
 • Pass flags to skip prompts: --printer, --pages, --bw, etc.
 • Use --yes (-y) for fully non-interactive printing.
"""

DUPLEX_WARNING = """
[!] MANUAL DUPLEX NOTICE [!]
If your printer does not support automatic double-sided printing,
you will need to manually RE-INSERT THE PAPER when prompted
by the printer hardware or system dialog.
"""

@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option("-d", "--printer", help="Target printer name.")
@click.option("-p", "--pages", help="Page range (e.g., '*', '1-5', '1,3,5').")
@click.option("-n", "--copies", type=int, help="Number of copies.")
@click.option("--bw", "color_mode", flag_value="Black & White", help="Print in Black & White.")
@click.option("--color", "color_mode", flag_value="Color", help="Print in Color.")
@click.option("--sides", type=click.Choice(["one-sided", "two-sided-long-edge", "two-sided-short-edge"], case_sensitive=False), help="Duplex mode.")
@click.option("--size", type=click.Choice(["A4", "Letter", "Legal", "A5"], case_sensitive=False), help="Paper size.")
@click.option("--orientation", type=click.Choice(["Auto", "Portrait", "Landscape"], case_sensitive=False), help="Page orientation.")
@click.option("--fit/--no-fit", default=None, help="Fit to page scaling.")
@click.option("-m/-nm", "--merge/--no-merge", default=None, help="Merge multiple files into one job.")
@click.option("-y", "--yes", is_flag=True, help="Skip confirmation prompt.")
@click.option("-o", "--output", help="Output path for 'Save as PDF' mode.")
def cli(paths, printer, pages, copies, color_mode, sides, size, orientation, fit, merge, yes, output):
    """An intuitive, interactive printing CLI."""
    if not paths:
        click.secho("Error: No files or directories provided.", fg="red")
        sys.exit(1)

    # Only show art/instructions if not in fully silent mode
    if not (yes and printer and pages):
        click.clear()
        click.echo(click.style(WELCOME_ART, fg="cyan", bold=True))
        click.echo(click.style(INSTRUCTIONS, fg="white"))
    
    files = collect_files(paths)
    if not files:
        click.secho("No supported files found in the provided paths.", fg="red")
        sys.exit(1)

    if not (yes and printer and pages):
        click.echo(click.style("-" * 50, fg="bright_black"))
        if len(files) == 1:
            click.echo(f"  Target File: {click.style(os.path.basename(files[0]), fg='green', bold=True)}")
        else:
            click.echo(f"  Target Files: {click.style(f'{len(files)} files found', fg='green', bold=True)}")
        click.echo(click.style("-" * 50, fg="bright_black"))
        click.echo("")

    check_os()
    
    printers = get_printers()
    if not printers:
        click.secho("No printers found and could not initialize a virtual PDF printer.", fg="red")
        sys.exit(1)

    # 1. Printer Selection
    if not printer:
        printer = questionary.select("Which printer would you like to use?", choices=printers).ask()
    elif printer not in printers:
        click.secho(f"Error: Printer '{printer}' not found.", fg="red")
        sys.exit(1)

    if not printer:
        return

    # 2. Batch Handling
    final_files = []
    temps_to_cleanup = []
    
    if len(files) > 1:
        if merge is None:
            merge = questionary.confirm(f"Would you like to merge all {len(files)} files into a single print job?", default=True).ask()
        
        if merge:
            converted_pdfs = []
            for f in files:
                target, was_conv = convert_to_pdf(f)
                converted_pdfs.append(target)
                if was_conv:
                    temps_to_cleanup.append(target)
            
            merged_pdf = os.path.join(tempfile.gettempdir(), f"print_cli_merged_{os.getpid()}.pdf")
            if merge_pdfs(converted_pdfs, merged_pdf):
                final_files = [merged_pdf]
                temps_to_cleanup.append(merged_pdf)
            else:
                final_files = files
        else:
            final_files = files
    else:
        final_files = files

    # 3. Page Selection
    if not pages:
        pages = questionary.text(
            "Which pages would you like to print?",
            default="*",
            instruction=" (Options: '*' for all, '1-5' for range, '1,3' for list)",
            validate=validate_page_range
        ).ask()
    else:
        val_res = validate_page_range(pages)
        if val_res is not True:
            click.secho(f"Error: {val_res}", fg="red")
            cleanup(temps_to_cleanup)
            sys.exit(1)

    if not pages:
        cleanup(temps_to_cleanup)
        return

    # 4. Color Mode
    if not color_mode and printer != PDF_PRINTER:
        color_mode = questionary.select("Select color mode:", choices=["Color", "Black & White"]).ask()
    elif not color_mode:
        color_mode = "Color"

    # 5. Duplex Mode
    if not sides and printer != PDF_PRINTER:
        sides_raw = questionary.select(
            "Select printing side:",
            choices=["One-Sided", "Double-Sided (Long-Edge)", "Double-Sided (Short-Edge)"]
        ).ask()
        if sides_raw == "One-Sided": sides = "one-sided"
        elif sides_raw == "Double-Sided (Long-Edge)": sides = "two-sided-long-edge"
        elif sides_raw == "Double-Sided (Short-Edge)": sides = "two-sided-short-edge"
    elif not sides:
        sides = "one-sided"

    # Map internal names for display and print_file
    duplex_map = {
        "one-sided": "One-Sided",
        "two-sided-long-edge": "Double-Sided (Long-Edge)",
        "two-sided-short-edge": "Double-Sided (Short-Edge)"
    }
    duplex_display = duplex_map.get(sides.lower(), "One-Sided") if sides else "One-Sided"

    if "two-sided" in sides.lower() and not yes:
        click.echo(click.style(DUPLEX_WARNING, fg="bright_yellow", bold=True))

    # 6. Orientation
    if not orientation:
        orientation = questionary.select("Select orientation:", choices=["Auto", "Portrait", "Landscape"]).ask()
    
    orientation = orientation.capitalize() if orientation else "Auto"

    # 7. Paper Size & Fit
    if not size and printer != PDF_PRINTER:
        size = questionary.select("Select paper size:", choices=["A4", "Letter", "Legal", "A5"]).ask()
    elif not size:
        size = "A4"
    size = size.upper() if size else "A4"

    if fit is None and printer != PDF_PRINTER:
        fit = questionary.confirm("Fit to page (auto-scale)?", default=False).ask()
    elif fit is None:
        fit = False

    # 8. Copies & Output Path
    if printer == PDF_PRINTER:
        if not output:
            output = questionary.text(
                "Enter output PDF file path:",
                default="merged_output.pdf" if len(final_files) == 1 and len(files) > 1 else f"printed_{os.path.basename(files[0])}.pdf",
            ).ask()
        if not output:
            cleanup(temps_to_cleanup)
            return
        if not output.lower().endswith(".pdf"):
            output += ".pdf"
        copies = 1
    else:
        if copies is None:
            copies_str = questionary.text(
                "How many copies?",
                default="1",
                validate=lambda val: val.isdigit() and int(val) > 0 or "Please enter a positive integer."
            ).ask()
            copies = int(copies_str) if copies_str else 1
        
    # Final confirmation
    file_label = f"{len(files)} files" if len(files) > 1 and len(final_files) > 1 else (os.path.basename(files[0]) if len(files) == 1 else "merged document")
    action = f"Save '{file_label}' as '{output}'" if printer == PDF_PRINTER else f"Print '{file_label}' to '{printer}' ({copies} copies each)"
    pages_msg = f" (Pages: {pages})" if pages != "*" else ""
    color_msg = f" [{color_mode}]" if printer != PDF_PRINTER else ""
    duplex_msg = f" [{duplex_display}]" if printer != PDF_PRINTER else ""
    layout_msg = f" [{size}, {orientation}, Fit: {fit}]" if printer != PDF_PRINTER else f" [{orientation}]"
    
    confirm = yes
    if not yes:
        confirm = questionary.confirm(f"{action}{pages_msg}{color_msg}{duplex_msg}{layout_msg}?").ask()

    if confirm:
        if platform.system() == "Windows" and printer != PDF_PRINTER and not yes:
            click.secho("\nNote: Some settings on Windows depend on your printer's default settings.", fg="yellow")

        for f in final_files:
            target, was_conv = convert_to_pdf(f)
            if was_conv:
                temps_to_cleanup.append(target)
            
            success = print_file(target, printer, copies, pages, color_mode, duplex_display, size, fit, orientation, output)
            if not success:
                click.secho(f"\nERROR: Failed to process '{os.path.basename(f)}'.", fg="red", bold=True)
            elif len(final_files) == 1:
                msg = f"File successfully saved to '{output}'." if printer == PDF_PRINTER else f"Job successfully submitted to '{printer}'."
                click.secho(f"\nSUCCESS: {msg}", fg="green", bold=True)
        
        if len(final_files) > 1:
            click.secho(f"\nSUCCESS: All {len(final_files)} jobs submitted to '{printer}'.", fg="green", bold=True)
    else:
        click.echo("Print job cancelled.")

    cleanup(temps_to_cleanup)

def cleanup(temp_files):
    """Deletes temporary files."""
    for f in temp_files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

if __name__ == "__main__":
    cli()
