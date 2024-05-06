from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import Image, Frame, Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
import json


def create_enhanced_tcg_cards(json_filepath, parchment_background_path):
    with open(json_filepath, 'r', encoding='utf-8') as file:
        cards = json.load(file)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CardTitle', parent=styles['Heading1'], fontSize=10, leading=12, spaceAfter=6,
                                 borderColor=colors.black,
                                 borderWidth=1, borderPadding=(2, 2, 2, 2), borderRadius=2, backColor=colors.lightgrey)
    text_style = ParagraphStyle('CardText', parent=styles['BodyText'], spaceAfter=6, borderColor=colors.black,
                                borderWidth=1, borderPadding=(4, 2, 4, 2), borderRadius=2, backColor=colors.whitesmoke)

    for card in cards:
        filename = f"figures/{card['pdf_output']}"
        c = canvas.Canvas(filename, pagesize=(2.48 * inch, 3.46 * inch))
        safe_area_x = (2.48 - 2.283) / 2 * inch
        safe_area_y = (3.46 - 3.27) / 2 * inch
        safe_width = 2.283 * inch
        safe_height = 3.27 * inch

        # Dimensions du cadre de l'image
        frame_width = safe_width  # Utiliser toute la largeur de la zone de sécurité
        frame_height = 1.53 * inch  # Hauteur augmentée pour une meilleure proportion

        # Draw parchment background
        parchment = ImageReader(parchment_background_path)
        c.drawImage(parchment, 0, 0, width=2.48 * inch, height=3.46 * inch)

        # Charger et dimensionner l'image
        img = ImageReader(card["image_path"])
        img_width, img_height = img.getSize()
        scale_factor = min(frame_width / img_width, frame_height / img_height)

        # Calculer la position centrée de l'image
        img_x = safe_area_x  # Utiliser directement la marge x pour aligner à gauche
        img_y = safe_area_y + safe_height - frame_height - 10 * mm  # Ajuster la position verticale

        c.drawImage(img, img_x, img_y, width=img_width * scale_factor, height=img_height * scale_factor)

        # Add title above the image
        title = Paragraph(card["title"], title_style)
        title_height = title.wrap(safe_width, 0.25 * inch)[1]
        title.drawOn(c, safe_area_x, img_y + frame_height + 6 * mm)

        # Add descriptive text with rounded border
        desc_text = Paragraph(card["text"], text_style)
        desc_text_height = desc_text.wrap(safe_width, safe_height - frame_height - title_height - 0.25 * inch)[1]
        desc_text.drawOn(c, safe_area_x, safe_area_y + 10)

        # Save the PDF
        c.save()


create_enhanced_tcg_cards("cards_data.json", "img/parchemin.png")
