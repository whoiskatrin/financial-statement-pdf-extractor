import os
import subprocess

import camelot
from PyPDF2 import PdfFileReader
from camelot.core import TableList


def total_pages(pdf):
    pdf_object = PdfFileReader(open(pdf, 'rb'))
    pages = ','.join([str(i) for i in list(range(pdf_object.getNumPages()))])
    return pages


def main():
    for pdf in os.listdir():
        file_name, file_extension = os.path.splitext(pdf)
        if file_extension == '.pdf':
            cmd = "pdfgrep -Pn '^(?s:(?=.*Revenue)|(?=.*Income))' " + pdf + " | awk -F\":\" '$0~\":\"{print $1}' | tr '\n' ','"
            pages = subprocess.check_output(cmd, shell=True).decode("utf-8")
            print(pdf)
            tables = camelot.read_pdf(pdf, flavor='stream', pages=pages, edge_tol=100)
            filtered = []
            for index, table in enumerate(tables):
                whitespace = tables[index].parsing_report.get('whitespace')
                if whitespace <= 25:
                    filtered.append(tables[index])
            filtered_tables = TableList(filtered)
            filtered_tables.export('test.xlsx', f='excel', compress=True)


if __name__ == "__main__":
    main()
