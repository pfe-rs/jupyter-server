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
margin = 25
padding = 45
font_size = 13

# Register font for users
if not isfile('users.ttf'):
    urlretrieve('https://pfe.rs/fonts/titillium/titillium-web-v10-latin-ext_latin-300.ttf', 'users.ttf')
pdfmetrics.registerFont(TTFont('PFE', 'users.ttf'))

i = 0
for user in data:
    c.setFont('PFE', font_size)
    line_y = h - margin - font_size * (i + 1) - padding * i
    c.drawString(margin, line_y, user['name'])
    c.drawString(w / 3, line_y, 'user: ' + user['username'])
    c.drawString(w / 3 * 2, line_y, 'pass: ' + user['password'])

    if i > 0:
        c.line(0, line_y + padding / 2, w, line_y + padding / 2)

    if line_y > padding + font_size + margin:
        i += 1
    else:
        c.showPage()
        i = 0

c.save()
