# -*- coding: utf-8 -*-

import docx2txt
import re
from os.path import join as join_path
from six import StringIO
import premailer, lesscpy
import os
import sys

ROOT = os.path.dirname(sys.argv[0])

def doc2html(doc_file_path):
    content = docx2txt.process(doc_file_path).replace("\t", "")
    texts = re.sub(r"[\n]+", "|", content).split("|")
    html = ""
    for text in texts:
        if text[0] == "#":
            #subtitle
            text = "<p class='subtitle'>" + text[1:] + "</p>\n"
        elif text[0] == "%":
            #picture note
            text = "<p class='note'>" + text[1:] + "</p>\n"
        elif text[0] == "&":
            #blockquote
            text = "<blockquote>" + text[1:] + "</blockquote>\n"
        else:
            #content
            content = text.split("*")
            for i in range(len(content) - 1):
                content[i] = content[i] + ("<strong>" if i % 2 == 0 else "</strong>")
            text = "<p class='content'>" + "".join(content) + "</p>\n"
        html += text
    return html

def compile_styles(file = join_path(ROOT, 'less', 'default.less')):
    fd = open(file, 'r', encoding='utf-8')
    raw_text = fd.read()
    fd.close()
    css = lesscpy.compile(StringIO(raw_text))
    fd = open(join_path(ROOT, 'css', 'default.css'), 'w', encoding='utf-8')
    fd.write(css)
    fd.close()

def pack_html(html):
    head = '''
<!DOCTYPE html><html lang="zh-cn">
<head>
<meta charset="UTF-8">
<title>result</title>
<link rel="stylesheet" type="text/css" href="{}">
</head>
<body>
<div class="wrapper">\n
'''.format(join_path(ROOT, 'css', 'default.css'))
    foot = '\n</div>\n</body>\n</html>'
    return head + html + foot


if __name__ == "__main__":
    html = doc2html("example.docx")
    result = premailer.transform(pack_html(html))

    fd = open("example.html", "w+")
    fd.write(result)
    fd.close()

