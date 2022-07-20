#!/usr/bin/env python

import json

from os.path import isfile
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from urllib.request import urlretrieve

with open('./users.json') as f:
    data = json.load(f)

c = Canvas('./users.pdf', pagesize=A4)

w, h = A4
margin = 30
padding = 45
font_size = 13

# Register font for users
if not isfile('titillium.ttf'):
    urlretrieve(
        'https://pfe.rs/fonts/titillium/titillium-web-v10-latin-ext_latin-300.ttf', 'titillium.ttf')
pdfmetrics.registerFont(TTFont('PFE', 'titillium.ttf'))

i = 0
for user in data:
    c.setFont('PFE', font_size)
    line_y_1 = h - margin - font_size * (i + 1) - padding * i
    line_y_2 = h - margin - font_size * (i + 2.5) - padding * i
    c.drawString(margin, line_y_1, user['name'])
    c.drawString(margin, line_y_2, 'username:')
    c.setFont('Courier', font_size)
    c.drawString(margin + 65, line_y_2, user['username'])
    c.setFont('PFE', font_size)
    c.drawString(w / 2, line_y_2, 'password:')
    c.setFont('Courier', font_size)
    c.drawString(w / 2 + 65, line_y_2, user['password'])

    if i > 0:
        c.line(0, line_y_1 + padding / 2, w, line_y_1 + padding / 2)

    if line_y_2 > padding + font_size + margin:
        i += 1
    else:
        c.showPage()
        i = 0

c.save()
