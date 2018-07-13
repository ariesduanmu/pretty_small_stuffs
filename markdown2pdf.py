# -*- coding: utf-8 -*-
#! /usr/bin/env python
import os
import sys
import argparse
from md2pdf import md2pdf
from PyPDF2 import PdfFileReader, PdfFileMerger


def target_files(basic_path, file_format):
    return sorted(name for name in os.listdir(basic_path) \
                  if not os.path.isdir(os.path.join(basic_path, name)) \
                     and name.endswith(file_format))

def convert(md_path, output_pdf_file="output.pdf"):
    if os.path.isdir(md_path):
        md_files = target_files(md_path, ".md")
        for md_file_name in md_files:
            pdf_file_name = "".join(md_file_name.split(".")[:-1]) + ".pdf"
            pdf_file_path = os.path.join(md_path, pdf_file_name)
            convert_mdfile(os.path.join(md_path, md_file_name), os.path.join(md_path, pdf_file_name))
    else:
        convert_mdfile(md_path, output_pdf_file)
    

def convert_mdfile(md_file, output_pdf_file):
    print(f"[+] MD name: {md_file}")
    print(f"[+] PDF name: {output_pdf_file}")
    print(f"[+] Converting...")
    md2pdf(output_pdf_file, md_file_path=md_file)

    print("[+] Convert finished")

def merge(basic_path, output_pdf_file):
    pdf_files = target_files(basic_path, ".pdf")
    merger = PdfFileMerger()
    for file in pdf_files:
        merger.append(PdfFileReader(os.path.join(basic_path, file)))
    merger.write(output_pdf_file)

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='markdown2pdf @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python markdown2pdf.py -e test.png -t howareyou
python prng_stego.py -e -r new test.png howareyou
python prng_stego.py -e -p password -m magic test.png -t howareyou
python prng_stego.py -e -p password -m magic test.png -t file_test.txt
python prng_stego.py --encrypt --password password --magic magic test.png -t "howareyou  some other text"

python prng_stego.py -d new_test.png
python prng_stego.py -d --rsa private.pem new_test.png
python prng_stego.py -d -p password -m magic new_test.png
python prng_stego.py --decrypt --password password --magic magic new_test.png

'''

                                        )
    parser.add_argument('-c','--convert', action="store_true", help='encrypt filename with text')
    parser.add_argument('-m','--merge', action="store_true", help='merge pdf files to one pdf')
    parser.add_argument('-D','--mdirectory', type=str, help='directory path with markdown files in it')
    parser.add_argument('-M','--markdown', type=str, help='markdown file path')
    parser.add_argument('-d','--pdirectory', type=str, help='directory path with pdf files in it')
    parser.add_argument('-o','--output', type=str, default = "output.pdf", help='output pdf file path')

    args = parser.parse_args()

    if args.convert ^ args.merge == False:
        parser.error('Incorrect convert/decrypt mode')
    if args.convert and (args.mdirectory is None and args.markdown is None):
        parser.error('Require -D <markdown file> or -M <directory with markdown files in it> in convert mode')
    if args.merge and args.pdirectory is None:
        parser.error('Require -d <directory with pdf files in it> in merge mode')
    return args

if __name__ == "__main__":
    args = parse_options()
    if args.convert:
        if args.mdirectory is not None:
            convert(args.mdirectory)
        elif args.markdown is not None:
            convert(args.markdown, args.output)
    elif args.merge:
        merge(args.pdirectory, args.output)

