# -*- coding: utf-8 -*-
#! /usr/bin/env python

from md2pdf import md2pdf
import os
from PyPDF2 import PdfFileReader, PdfFileMerger

def target_files(basic_path, file_format):
    chapters = sorted(name for name in os.listdir(basic_path) \
                if os.path.isdir(os.path.join(basic_path, name)))
    print(f"[+] Chapters: {chapters}")
    files = []
    for chapter in chapters:
        path = os.path.join(basic_path, chapter)
        for file in os.listdir(path):
            if file.endswith(file_format):
                files.append([path, file])
    return files


def convert(basic_path):
    md_files = target_files(basic_path, ".md")
    for path, file in md_files:
        pdf_file_name = "".join(file.split(".")[:-1]) + ".pdf"
        print(f"[+] MD name: {file}")
        print(f"[+] PDF name: {pdf_file_name}")
        print(f"[+] Converting...")
        md2pdf(os.path.join(path, pdf_file_name), md_file_path=os.path.join(path, file), base_url=path)

    print("[+] Convert finished")

def merge_pdf(basic_path, output_pdf_name):
    pdf_files = target_files(basic_path, ".pdf")
    merger = PdfFileMerger()
    for path, file in pdf_files:
        merger.append(PdfFileReader(os.path.join(path, file)))
    merger.write(output_pdf_name)

if __name__ == "__main__":
    basic_path = 'zh-cn'
    convert(basic_path)
    merge_pdf(basic_path, "learnhaskell.pdf")