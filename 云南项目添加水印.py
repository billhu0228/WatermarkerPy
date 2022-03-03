import math
import os

from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pytesseract
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib import colors
from wand.color import Color

from PDFMerger import AddWaterMarker
from src.Functions import *

if __name__ == "__main__":
    # inputfile = "./input/210807_A8L01.pdf"
    input_dir = "./input/wyz/"
    out_path = "./bin/wyz/"
    wmark_file="./data/markwyz.pdf"
    for file in os.listdir(input_dir):
        input_pdf=os.path.join(input_dir,file)
        out_filename = os.path.join(out_path, file + "_J.pdf")
        out_pdf = PdfFileWriter()
        src_pdf = PdfFileReader(open(input_pdf, 'rb'), strict=False)
        numpage = len(src_pdf.pages)
        for i, pg in enumerate(src_pdf.pages):
            cur_pg = pg
            dst_pdf = PdfFileWriter()
            dst_pdf.addPage(cur_pg)
            pdf_bytes = io.BytesIO()
            dst_pdf.write(pdf_bytes)
            pdf_bytes.seek(0)
            img = Image(file=pdf_bytes, resolution=120)
            img.alpha_channel = 'remove'
            val = average_blue(img, x0=151, y0=1338, w=41, h=1)

            wm = PdfFileReader(open(wmark_file, 'rb'), strict=False).getPage(0)
            wm_w, wm_h = wm['/MediaBox'][2:]
            cur_pg_w, cur_pg_h = cur_pg['/MediaBox'][2:]
            if cur_pg_w > cur_pg_h:  # A
                if wm_w > wm_h:  # A
                    rotation = math.radians(0)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               0, 0]
                else:  # B
                    rotation = math.radians(270)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               0, cur_pg_h]
            else:  # B
                if wm_w > wm_h:  # A
                    rotation = math.radians(270)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               0, cur_pg_h]
                else:  # B
                    rotation = math.radians(180)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               cur_pg_w, cur_pg_h]
            cur_pg.mergeTransformedPage(wm, MatrixA)
            print(file + " : 水印添加")
            out_pdf.addPage(cur_pg)
            print("页面 %i / %i 输出.." % (i, numpage))
        with open(out_filename, 'wb') as f:
            out_pdf.write(f)

    # dir, tmp = os.path.split(inputfile)
    # ext = tmp.split('.')[-1]
    # filename = tmp.replace('.%s' % ext, '')
