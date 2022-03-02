from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pytesseract
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib import colors
from wand.color import Color

from PDFMerger import AddWaterMarker,AddWaterMarkerByList
from Functions import *

if __name__ == "__main__":
    pdfmetrics.registerFont(TTFont('Arial', 'arial07.ttf'))
    addMapping('Arial', 0, 0, 'Arial')
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    tesseract_config = r"""-c tessedit_char_whitelist=0123456789ABCDEGHIJKLMNPRSW/"""

    inputfile = "./input/test.pdf"
    page_add = {}
    with Image(filename=inputfile, resolution=120, background=Color('white')) as source:
        images = source.sequence
        pages = len(images)
        for i in range(pages):
            img = Image(images[i])
            img.alpha_channel = 'remove'
            val = average_blue(img, x0=151, y0=1338, w=41, h=1)
            print(val)
            if val < 249:
                ret = cut(img, 1660, 1290, 270, 25)
                s = pytesseract.image_to_string(ret, config=tesseract_config)
                page_add[i] = s.strip() + "J"
                # create_watermark(s+"J")
                # AddWaterMarker(inputfile, "./data/mark.pdf", "./bin")
            # print(s)
            # ret.save(filename="%i.png" % i)
    AddWaterMarkerByList(inputfile, page_add, "./bin")
    print("进程终止..")
