import os
import tempfile
from fpdf import FPDF
from PIL import Image
from pypdf import PdfWriter

SUPPORTED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".txt", ".md", ".log"]

def convert_to_pdf(file_path):
    """
    Converts supported file types (images, text) to a temporary PDF.
    Returns the path to the temporary PDF or the original path if already PDF.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return file_path, False

    temp_pdf = os.path.join(tempfile.gettempdir(), f"print_cli_conv_{os.getpid()}_{os.urandom(4).hex()}.pdf")
    
    try:
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            return convert_image_to_pdf(file_path, temp_pdf), True
        elif ext in [".txt", ".md", ".log"]:
            return convert_text_to_pdf(file_path, temp_pdf), True
        else:
            return file_path, False
    except Exception as e:
        print(f"Conversion error for {file_path}: {e}")
        return file_path, False

def convert_image_to_pdf(image_path, output_path):
    """Converts an image to a PDF page, fitting it to A4."""
    pdf = FPDF()
    pdf.add_page()
    
    with Image.open(image_path) as img:
        img_width, img_height = img.size
    
    max_w = 190
    max_h = 277
    
    ratio = min(max_w / img_width, max_h / img_height)
    new_w = img_width * ratio
    new_h = img_height * ratio
    
    x = (210 - new_w) / 2
    y = (297 - new_h) / 2
    
    pdf.image(image_path, x=x, y=y, w=new_w, h=new_h)
    pdf.output(output_path)
    return output_path

def convert_text_to_pdf(text_path, output_path):
    """Converts a text file to a PDF with basic formatting."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    
    with open(text_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            pdf.multi_cell(0, 5, txt=line.rstrip())
            
    pdf.output(output_path)
    return output_path

def merge_pdfs(pdf_paths, output_path):
    """Merges multiple PDFs into a single file."""
    merger = PdfWriter()
    try:
        for pdf in pdf_paths:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        return output_path
    except Exception as e:
        print(f"Merge error: {e}")
        return None

def collect_files(paths):
    """Expands directories and filters for supported files."""
    files = []
    for p in paths:
        if os.path.isfile(p):
            if os.path.splitext(p)[1].lower() in SUPPORTED_EXTENSIONS:
                files.append(p)
        elif os.path.isdir(p):
            for root, _, filenames in os.walk(p):
                for f in filenames:
                    if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS:
                        files.append(os.path.join(root, f))
    return sorted(files)
