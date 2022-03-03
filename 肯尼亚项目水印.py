import math
import os

from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pytesseract
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib import colors
from wand.color import Color

from src.functions import *

if __name__ == "__main__":
    input_file = "./input/210807_A8L01.pdf"
    out_path = "./bin/"
    dir, tmp = os.path.split(input_file)
    ext = tmp.split('.')[-1]
    filename = tmp.replace('.%s' % ext, '')
    out_filename = os.path.join(out_path, filename + "_J.pdf")

    pdfmetrics.registerFont(TTFont('Arial', 'arial07.ttf'))
    addMapping('Arial', 0, 0, 'Arial')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    tesseract_config = r"""-c tessedit_char_whitelist=0123456789ABCDEGHIJKLMNPRSW/-"""

    out_pdf = PdfFileWriter()
    src_pdf = PdfFileReader(open(input_file, 'rb'), strict=False)
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
        if val < 249:
            ret = cut(img, 1660, 1290, 270, 25)
            s = pytesseract.image_to_string(ret, config=tesseract_config)
            s = correct_no(s, "1", i)
            create_watermark(s)
            print(s + " : 水印生成")
            wm = PdfFileReader(open("./data/mark.pdf", 'rb'), strict=False).getPage(0)
            wm_w, wm_h = wm['/MediaBox'][2:]
            cur_pg_w, cur_pg_h = cur_pg['/MediaBox'][2:]
            if cur_pg_w > cur_pg_h:  # A
                if wm_w > wm_h:  # A
                    rotation = math.radians(0)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               0, 0]
                else:  # B
                    rotation = math.radians(90)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               cur_pg_w, 0]
            else:  # B
                if wm_w > wm_h:  # A
                    rotation = math.radians(270)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               0, cur_pg_h]
                else:  # B
                    rotation = math.radians(0)
                    MatrixA = [math.cos(rotation), math.sin(rotation),
                               -math.sin(rotation), math.cos(rotation),
                               0, 0]
            cur_pg.mergeTransformedPage(wm, MatrixA)
            print(s + " : 水印添加")
        else:
            pass
        out_pdf.addPage(cur_pg)
        print("页面 %i / %i 输出.." % (i, numpage))
    with open(out_filename, 'wb') as f:
        out_pdf.write(f)
    pass
