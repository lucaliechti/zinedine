# prerequisite: pip install pypdf2
# released under the WTFPL: http://www.wtfpl.net/
# author: luca.liechti@protonmail.ch
# version 0.0.3

from math import ceil
from sys import argv, exit
from PyPDF2 import PdfReader, PdfWriter
from reorder import reorder_pages

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

def extract_dimensions(page):
    mediabox = page.mediabox
    return mediabox.height, mediabox.width

def extractDocumentSize(input_pages):
    num_pages = len(input_pages)
    if num_pages < 1:
        print('Empty or invalid PDF. Exiting.')
        exit(1)
    if not num_pages % 4 == 0:
        print('Page number is not divisible by 4, will append ' + str(4 - (num_pages % 4)) + ' blank page(s).')
        extract_dimensions(input_pdf.pages[0])
    return num_pages

def add_blank_page(pdf_writer):
    pdf_writer.add_blank_page(width = page_width, height = page_height)

def add_pages_in_new_order(pdf_writer, new_order):
    page_height, page_width = extract_dimensions(input_pages[0])
    for i in range(len(new_order)):
        if new_order[i] == -1:
            pdf_writer.add_blank_page(width = page_width, height = page_height)
        else:
            pdf_writer.add_page(input_pages[new_order[i]])

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
input_pages = input_pdf.pages

num_pages = extractDocumentSize(input_pages)
new_order = reorder_pages(num_pages)

pdf_writer = PdfWriter()
add_pages_in_new_order(pdf_writer, new_order)
write_reordered_file(pdf_writer, output_filename)
pdf_writer.close()

print('PDF successfully reordered to zine format.')
