import os
import tempfile
from fpdf import FPDF
from PIL import Image

def convert_to_pdf(file_path):
    """
    Converts supported file types (images, text) to a temporary PDF.
    Returns the path to the temporary PDF or the original path if already PDF.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return file_path, False

    temp_pdf = os.path.join(tempfile.gettempdir(), f"print_cli_conv_{os.getpid()}.pdf")
    
    try:
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            return convert_image_to_pdf(file_path, temp_pdf), True
        elif ext in [".txt", ".md", ".log"]:
            return convert_text_to_pdf(file_path, temp_pdf), True
        else:
            # For unsupported types, just return the original and let the OS handler try
            return file_path, False
    except Exception as e:
        print(f"Conversion error: {e}")
        return file_path, False

def convert_image_to_pdf(image_path, output_path):
    """Converts an image to a PDF page, fitting it to A4."""
    pdf = FPDF()
    pdf.add_page()
    
    # Get image dimensions using PIL to handle aspect ratio
    with Image.open(image_path) as img:
        img_width, img_height = img.size
    
    # A4 dimensions in mm: 210 x 297
    # Max width/height with 10mm margins
    max_w = 190
    max_h = 277
    
    # Calculate scaling to fit within A4 margins
    ratio = min(max_w / img_width, max_h / img_height)
    new_w = img_width * ratio
    new_h = img_height * ratio
    
    # Center image
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
            # multi_cell handles wrapping and newlines
            pdf.multi_cell(0, 5, txt=line.rstrip())
            
    pdf.output(output_path)
    return output_path
