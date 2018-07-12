# -*- coding: utf-8 -*-
#! /usr/bin/env python
import os
import sys
import argparse
from md2pdf import md2pdf
from PyPDF2 import PdfFileReader, PdfFileMerger

def convert(md_filename, pdf_filename="output.pdf"):
    if not os.path.exists(md_filename):
        print("Markdown文件不存在")
        sys.exit(0)

    print(f"[+] MD name: {md_filename}")
    print(f"[+] PDF name: {pdf_filename}")
    print(f"[+] Converting...")
    md2pdf(pdf_filename, md_file_path=md_filename)

    print("[+] Convert finished")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage [exe] [markdown file path] [output pdf file path]")
        sys.exit(0)
    md_filename = sys.argv[1]
    pdf_filename = sys.argv[2]
    convert(md_filename, pdf_filename)
    