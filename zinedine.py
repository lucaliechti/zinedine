# prerequisite: pip install pypdf2
# released under the WTFPL: http://www.wtfpl.net/
# author: luca.liechti@protonmail.ch
# version 0.0.2

from math import ceil
from sys import argv, exit
from PyPDF2 import PdfReader, PdfWriter

page_height = None
page_width = None
num_pages = None
num_sheets = None

def open_file(input_filename):
    file = None
    try:
        file = open(input_filename, 'rb')
    except Exception as e:
        print(e + '. Exiting')
        exit(1)
    return file

def read_pdf(file):
    try:
        pdf = PdfReader(file)
    except Exception as e:
        print(e + '. Exiting')
        exit(1)
    return pdf

def extractDocumentSize(pdf):
    num_pages = len(pdf.pages)
    if num_pages < 1:
        print('Empty or invalid PDF. Exiting.')
        exit(1)
    num_sheets = ceil(num_pages / 4)
    return num_pages, num_sheets

def extract_dimensions(page):
    mediabox = page.mediabox
    return mediabox.height, mediabox.width

def add_blank_page(pdf_writer):
    pdf_writer.add_blank_page(width = page_width, height = page_height)

def rearrange_max_4_pages(pdf_writer, pdf):
    pdf_writer.add_page(pdf.pages[3]) if 4 <= num_pages else add_blank_page(pdf_writer)
    pdf_writer.add_page(pdf.pages[0])
    pdf_writer.add_page(pdf.pages[1]) if 2 <= num_pages else add_blank_page(pdf_writer)
    pdf_writer.add_page(pdf.pages[2]) if 3 <= num_pages else add_blank_page(pdf_writer)

def rearrange_min_5_pages(pdf_writer, pdf):
    pdf_writer.add_page(pdf.pages[4 * num_sheets - 1]) if 4 * num_sheets - 1 < num_pages else add_blank_page(pdf_writer)
    pdf_writer.add_page(pdf.pages[0])
    pdf_writer.add_page(pdf.pages[1])
    pdf_writer.add_page(pdf.pages[4 * num_sheets - 2]) if 4 * num_sheets - 2 < num_pages else add_blank_page(pdf_writer)
    pdf_writer.add_page(pdf.pages[4 * num_sheets - 3]) if 4 * num_sheets - 3 < num_pages else add_blank_page(pdf_writer)
    pdf_writer.add_page(pdf.pages[2])
    pdf_writer.add_page(pdf.pages[3])
    pdf_writer.add_page(pdf.pages[4 * num_sheets - 4])

    if num_pages > 8:
        for sheet in range(2, num_sheets):
            page1 = num_pages - (2 * sheet) - 1
            page2 = sheet * 2
            page3 = sheet * 2 + 1
            page4 = num_pages - (2 * sheet) - 2

            pdf_writer.add_page(pdf.pages[page1])
            pdf_writer.add_page(pdf.pages[page2])
            pdf_writer.add_page(pdf.pages[page3])
            pdf_writer.add_page(pdf.pages[page4])

def write_reordered_file(pdf_writer, output_filename):
    with open(output_filename, 'wb') as output:
        pdf_writer.write(output)

if not len(argv) == 3:
    print('Please provide exactly two arguments, first the path to your PDF and second the output path where the rearranged PDF.')
    exit(1)

input_filename = argv[1]
output_filename = argv[2]

input_file = open_file(input_filename)
input_pdf = read_pdf(input_file)

num_pages, num_sheets = extractDocumentSize(input_pdf)
if not num_pages % 4 == 0:
    print('Page number is not divisible by 4, will append ' + str(4 - (num_pages % 4)) + ' blank page(s) .')
    page_height, page_width = extract_dimensions(input_pdf.pages[0])

pdf_writer = PdfWriter()

if num_pages <= 4:
    rearrange_max_4_pages(pdf_writer, input_pdf)
else:
    rearrange_min_5_pages(pdf_writer, input_pdf)

write_reordered_file(pdf_writer, output_filename)

pdf_writer.close()
