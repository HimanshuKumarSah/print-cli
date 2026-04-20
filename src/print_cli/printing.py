import subprocess
import platform
import sys
import os
import shutil
import tempfile
import re

# Special printer name for saving as PDF
PDF_PRINTER = "Print to PDF (Save as File)"

def check_os():
    """Ensure the OS is supported."""
    os_type = platform.system()
    if os_type not in ["Linux", "Darwin", "Windows"]:
        print(f"Error: {os_type} is not supported.")
        sys.exit(1)

def get_printers():
    """Discover available printers and always include 'Print to PDF'."""
    os_type = platform.system()
    printers = []
    
    try:
        if os_type in ["Linux", "Darwin"]:
            output = subprocess.check_output(["lpstat", "-a"], text=True, stderr=subprocess.DEVNULL)
            for line in output.splitlines():
                if line:
                    parts = line.split()
                    if parts:
                        printers.append(parts[0])
        elif os_type == "Windows":
            cmd = ["powershell", "-Command", "Get-Printer | Select-Object -ExpandProperty Name"]
            output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
            printers = [line.strip() for line in output.splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Always add our custom 'Print to PDF' option at the top for consistency
    if PDF_PRINTER not in printers:
        printers.insert(0, PDF_PRINTER)
    
    return printers

def validate_page_range(val):
    """Validate page range string (*, 1-5, 1,3,5, etc.)."""
    if val == "*":
        return True
    # Regex for lists, ranges, and individual numbers: e.g., "1-3,5,7-10"
    pattern = r'^(\d+(-\d*)?)(,(\d+(-\d*)?))*$'
    if re.match(pattern, val.replace(" ", "")):
        return True
    return "Please enter a valid page range (e.g., *, 1-5, 1,3,5)."

def print_file(file_path, printer_name, copies=1, page_range="*", color_mode="Color", duplex_mode="One-Sided", paper_size="A4", fit_to_page=False, orientation="Auto", output_path=None):
    """Execute the print job with optional page selection, color mode, duplex mode, scaling, and orientation."""
    os_type = platform.system()
    file_path = os.path.abspath(file_path)
    
    if printer_name == PDF_PRINTER:
        if not output_path:
            return False
        try:
            if page_range == "*" and not fit_to_page and orientation == "Auto":
                shutil.copy2(file_path, output_path)
                return True
            else:
                if os_type in ["Linux", "Darwin"]:
                    print("Page selection and orientation for 'Save as File' is currently only supported on Windows.")
                    return False
                elif os_type == "Windows":
                    cmd = [
                        "msedge.exe", 
                        "--headless", 
                        f"--print-to-pdf={output_path}", 
                        "--print-to-pdf-no-header", 
                        f"--pages={page_range}", 
                    ]
                    if orientation == "Landscape":
                        cmd.append("--landscape")
                    cmd.append(f"file:///{file_path}")
                    subprocess.check_call(cmd)
                    return True
        except Exception as e:
            print(f"Error saving to PDF: {e}")
            return False

    try:
        if os_type in ["Linux", "Darwin"]:
            command = ["lp", "-d", printer_name, "-n", str(copies)]
            
            # Color mode
            if color_mode == "Black & White":
                command.extend(["-o", "ColorModel=Gray"])
            else:
                command.extend(["-o", "ColorModel=Color"])
            
            # Duplex mode
            if duplex_mode == "Double-Sided (Long-Edge)":
                command.extend(["-o", "sides=two-sided-long-edge"])
            elif duplex_mode == "Double-Sided (Short-Edge)":
                command.extend(["-o", "sides=two-sided-short-edge"])
            else:
                command.extend(["-o", "sides=one-sided"])
            
            # Paper size
            command.extend(["-o", f"media={paper_size}"])
            
            # Fit to page
            if fit_to_page:
                command.extend(["-o", "fit-to-page"])

            # Orientation
            if orientation == "Landscape":
                command.extend(["-o", "landscape"])
            elif orientation == "Portrait":
                command.extend(["-o", "portrait"])
                
            if page_range != "*":
                command.extend(["-P", page_range])
            command.append(file_path)
            subprocess.check_call(command)
            return True
        elif os_type == "Windows":
            target_file = file_path
            temp_pdf = None
            
            # If specific pages or orientation are requested on Windows, we MUST create a temp PDF first
            if page_range != "*" or orientation != "Auto":
                temp_dir = tempfile.gettempdir()
                temp_pdf = os.path.join(temp_dir, f"print_subset_{os.getpid()}.pdf")
                try:
                    cmd = [
                        "msedge.exe", 
                        "--headless", 
                        f"--print-to-pdf={temp_pdf}", 
                        "--print-to-pdf-no-header", 
                        f"--pages={page_range}", 
                    ]
                    if orientation == "Landscape":
                        cmd.append("--landscape")
                    cmd.append(f"file:///{file_path}")
                    subprocess.check_call(cmd)
                    target_file = temp_pdf
                except Exception as e:
                    print(f"Error extracting pages/orientation via Edge: {e}")
                    return False

            try:
                for _ in range(copies):
                    cmd = [
                        "powershell", 
                        "-Command", 
                        f"Start-Process -FilePath '{target_file}' -Verb PrintTo -ArgumentList '{printer_name}' -PassThru"
                    ]
                    subprocess.check_call(cmd)
                return True
            finally:
                if temp_pdf and os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
    except subprocess.CalledProcessError as e:
        print(f"Error executing print command: {e}")
        return False
    return False
