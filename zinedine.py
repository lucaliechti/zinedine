# prerequisite: pip install pypdf2

import math
import sys
from PyPDF2 import PdfReader, PdfWriter

def reorder_to_zine_layout(input_filename, output_filename):
    with open(input_filename, 'rb') as file:
        pdf = PdfReader(file)
        box = pdf.pages[0].mediabox
        page_width = box.width
        page_height = box.height
        num_pages = len(pdf.pages)
        num_sheets = math.ceil(num_pages / 4)

        pdf_writer = PdfWriter()

	# assumption: number of pages >= 5
        pdf_writer.add_page(pdf.pages[4 * num_sheets - 1]) if 4 * num_sheets - 1 < num_pages else pdf_writer.add_blank_page(width = page_width, height = page_height)
        pdf_writer.add_page(pdf.pages[0])
        pdf_writer.add_page(pdf.pages[1])
        pdf_writer.add_page(pdf.pages[4 * num_sheets - 2]) if 4 * num_sheets - 2 < num_pages else pdf_writer.add_blank_page(width = page_width, height = page_height)
        pdf_writer.add_page(pdf.pages[4 * num_sheets - 3]) if 4 * num_sheets - 3 < num_pages else pdf_writer.add_blank_page(width = page_width, height = page_height)
        pdf_writer.add_page(pdf.pages[2])
        pdf_writer.add_page(pdf.pages[3])
        pdf_writer.add_page(pdf.pages[4 * num_sheets - 4])

        if num_sheets > 2:
            for sheet in range(2, num_sheets):
                page1 = num_pages - (2 * sheet)
                page2 = sheet * 2
                page3 = sheet * 2 + 1
                page4 = num_pages - (2 * sheet) - 1

                pdf_writer.add_page(pdf.pages[page1])
                pdf_writer.add_page(pdf.pages[page2])
                pdf_writer.add_page(pdf.pages[page3])
                pdf_writer.add_page(pdf.pages[page4])

        with open(output_filename, 'wb') as output:
            pdf_writer.write(output)

input_filename = sys.argv[1]
output_filename = sys.argv[2]
reorder_to_zine_layout(input_filename, output_filename)
