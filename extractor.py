import os
import argparse
import subprocess
import logging
from multiprocessing import Pool

import camelot
from PyPDF2 import PdfFileReader
from camelot.core import TableList

def total_pages(pdf):
    with open(pdf, 'rb') as file:
        pdf_object = PdfFileReader(file)
        pages = ','.join([str(i) for i in range(pdf_object.getNumPages())])
    return pages

def extract_tables(pdf, pattern):
    try:
        cmd = f"pdfgrep -Pn '{pattern}' {pdf} | awk -F\":\" '$0~\":\"{{print $1}}' | tr '\n' ','"
        pages = subprocess.check_output(cmd, shell=True).decode("utf-8")
        if not pages:
            logging.warning(f"No matching pages found in {pdf}")
            return

        tables = camelot.read_pdf(pdf, flavor='stream', pages=pages, edge_tol=100)
        filtered = []
        for index, table in enumerate(tables):
            whitespace = tables[index].parsing_report.get('whitespace')
            if whitespace <= 25:
                filtered.append(tables[index])
        filtered_tables = TableList(filtered)
        filtered_tables.export(f"{os.path.splitext(pdf)[0]}.xlsx", f='excel', compress=True)
        logging.info(f"Processed {pdf}")
    except Exception as e:
        logging.error(f"Error processing {pdf}: {str(e)}")

def main(input_dir, output_dir, processes, pattern):
    logging.basicConfig(filename='extract_tables.log', level=logging.INFO)
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.lower().endswith('.pdf')]

    with Pool(processes=processes) as pool:
        pool.starmap(extract_tables, [(pdf, pattern) for pdf in pdf_files])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from PDF files containing 'Revenue' or 'Income'")
    parser.add_argument("-i", "--input", required=True, help="Input directory containing PDF files")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save the extracted tables")
    parser.add_argument("-p", "--processes", type=int, default=os.cpu_count(), help="Number of parallel processes")
    parser.add_argument("-r", "--regex", default='^(?s:(?=.*Revenue)|(?=.*Income))', help="Regex pattern to search in PDF files")
    args = parser.parse_args()

    main(args.input, args.output, args.processes, args.regex)
