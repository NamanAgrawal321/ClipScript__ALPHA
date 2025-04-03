import re
import requests
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image as PilImage

# Register a Hindi-supporting TrueType font.
# Make sure 'NotoSansDevanagari-Regular.ttf' is in your working directory.
def document(content,name):
    pdfmetrics.registerFont(TTFont('NotoSansDevanagari', 'NotoSansDevanagari-Regular.ttf'))

    # Create a custom style for Hindi text using the registered font
    styles = getSampleStyleSheet()
    hindi_style = ParagraphStyle(
        'Hindi',
        parent=styles['Normal'],
        fontName='NotoSansDevanagari',
        fontSize=12,
        leading=14,
    )

    # You can also define a style for English text if needed
    english_style = styles['Normal']

    def is_image_url(text_line):
        # Check if the line is a URL ending with common image extensions.
        return re.match(r'^https?://.*\.(webp|jpg|jpeg|png)$', text_line.strip(), re.IGNORECASE)

    # Create the PDF document
    pdf_file = f"{name}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)


    story = []
    page_width, page_height = A4
    max_width = page_width * 0.25
    max_height = page_height * 0.25  # Optional: restrict height

    # Process the content line by line
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        if is_image_url(line):
            try:
                response = requests.get(line)
                response.raise_for_status()
                image_data = BytesIO(response.content)
                
                # Open image with Pillow to get its dimensions
                pil_image = PilImage.open(image_data)
                orig_width, orig_height = pil_image.size
                
                # Calculate scaling factor to fit the image within max_width/max_height
                scale = min(max_width / orig_width, max_height / orig_height, 1)
                draw_width = orig_width * scale
                draw_height = orig_height * scale
                
                # Reset the BytesIO stream for ReportLab
                image_data.seek(0)
                img = Image(image_data, width=draw_width, height=draw_height)
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                error_paragraph = Paragraph(f"Error loading image: {e}", english_style)
                story.append(error_paragraph)
                story.append(Spacer(1, 0.2 * inch))
        else:
            # Decide which style to use based on content.
            # Here, if the text contains Hindi characters, we use the Hindi style.
            if re.search(r'[\u0900-\u097F]', line):
                para = Paragraph(line, hindi_style)
            else:
                para = Paragraph(line, english_style)
            story.append(para)
            story.append(Spacer(1, 0.2 * inch))

    # Build the PDF
    doc.build(story)
    print(f"PDF saved as {pdf_file}")
