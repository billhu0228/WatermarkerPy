import io
import math
import os
import re

import numpy as np
from PIL import Image as PImage
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.pdf import PageObject
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from wand.image import Image


def cut(img: 'Image', x0: int, y0: int, w: int, h: int):
    ret = img.clone()[x0:x0 + w, y0:y0 + h]
    img_buffer = np.asarray(bytearray(ret.make_blob(format='png')), dtype='uint8')
    bytesio = io.BytesIO(img_buffer)
    pil_img = PImage.open(bytesio)
    return pil_img


def correct_no_rf(s: str):
    s = s.strip()
    if s.__contains__('-'):
        s = s[0:-2]
    if "BR" in s:
        tmp = re.split("BR", s)
    else:
        raise Exception("错误：%s" % s)
    news = "NEP/CD/RFD" + "/BR/" + tmp[-1][1:]
    news += "J"
    return news


def correct_no(s: str, secn, i=0):
    s = s.strip()
    if s.__contains__('-'):
        s = s[0:-2]
    if "BR" in s:
        tmp = re.split("BR", s)
    else:
        raise Exception("错误：%s" % s)
    news = "NEP/CD/SEC" + secn + "/BR/" + tmp[-1][1:]
    news += "J"
    return news


def create_watermark(content):
    """水印信息"""
    # 默认大小为21cm*29.7cm
    file_name = "./data/mark.pdf"
    c = canvas.Canvas(file_name, pagesize=(42 * cm, 29.7 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    # c.translate( * cm, 5 * cm)
    # 设置字体
    c.setFont("Arial", 11.6)
    # 画几个文本,注意坐标系旋转的影响
    # c.drawString((35+41)*0.5*cm,29.7*cm, content)
    c.setFillColorRGB(1, 1, 1)
    c.rect((35 + 0.5) * cm, (1.75 + 0.12) * cm, 5 * cm, 0.49 * cm, fill=1, stroke=0)
    c.rect((35 + 0.5) * cm, (1.0 + 0.2) * cm, 5 * cm, 0.49 * cm, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)
    # c.drawString(38 * cm, 2.125 * cm, content)
    c.drawCentredString(38 * cm, 2.035 * cm, content, charSpace=1)
    c.drawCentredString(38 * cm, 1.275 * cm, "DEC. 2021", charSpace=1)
    # 关闭并保存pdf文件
    c.save()
    return file_name


def average_blue(img: 'Image', x0: int, y0: int, w: int, h: int) -> float:
    """
    计算图像一块区域的平均蓝色
    :param img:
    :param x0:
    :param y0:
    :param w:
    :param h:
    :return:
    """
    mat = []
    for j in range(h):
        line = []
        for i in range(w):
            line.append(img[x0 + i, y0 + j].blue_int8)
        mat.append(line)
    men = np.array(mat).mean()
    if img.colorspace == 'cmyk':
        ret = 255 - men
    else:
        ret = men
    return ret


def search_file(path, ext):
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            for k in search_file(os.path.join(path, item), ext):
                yield k
        else:
            if item.endswith(ext):
                yield os.path.join(path, item)


def add_watermark_by_page(page: PageObject, water_mark: PageObject,
                          rot_deg=0, dx=0, dy=0,
                          ) -> PageObject:
    rotation = math.radians(rot_deg)
    Matrix90 = (math.cos(rotation), math.sin(rotation),
                -math.sin(rotation), math.cos(rotation),
                dx, dy)
    cur_pg = page
    wm = water_mark
    if list(cur_pg.keys()).__contains__("/Rotate") and cur_pg["/Rotate"] == 270:
        cur_pg.mergeTransformedPage(wm, Matrix90)
    else:
        cur_pg.mergePage(wm)
    return cur_pg


def add_watermark_by_list(pdfs: str, page_dict, water_mark: str, out_path: str = "", out_name='', suffix: str = "_out",
                          auto_adjust=True,
                          rot_deg=0, dx=0, dy=0,
                          ):
    """
    :param pdfs: 原文件,可含有多个文件
    :param water_mark: 水印文件, 仅读取第一个文件
    :param out_path: 输出路径, 可为空
    :param out_name: 输出文件名称, 可为空
    :param suffix: 后缀, 无后缀且同路径时将替换源文件
    :param auto_adjust: 是否自动调整位置, 默认Ture
    :param rot_deg: 转动
    :param dx: x平移
    :param dy: y平移
    :return: None
    """
    out_pdf = PdfFileWriter()
    dir, tmp = os.path.split(pdfs)
    ext = tmp.split('.')[-1]
    filename = tmp.replace('.%s' % ext, '')
    if out_name == "":
        out_name = filename
    else:
        out_name = out_name.split('.')[0]
    if out_path == "":
        out_path = os.path.join(dir, out_name + ".pdf")
    else:
        out_path = os.path.join(out_path, out_name + ".pdf")

    src_pdf = PdfFileReader(open(pdfs, 'rb'), strict=False)
    pages_to_add = page_dict.keys()
    for ii, pg in enumerate(src_pdf.pages):
        cur_pg = pg
        if ii in pages_to_add:
            create_watermark(page_dict[ii])
            print(page_dict[ii] + "水印生成")
            wm = PdfFileReader(open("./data/mark.pdf", 'rb'), strict=False).getPage(0)
            wm_w, wm_h = wm['/MediaBox'][2:]
            cur_pg_w, cur_pg_h = cur_pg['/MediaBox'][2:]
            if not auto_adjust:
                rotation = math.radians(rot_deg)
                MatrixA = [math.cos(rotation), math.sin(rotation),
                           -math.sin(rotation), math.cos(rotation),
                           dx, dy]
            else:  # 自动调整
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
            print(page_dict[ii] + "水印添加")
        else:
            pass
        out_pdf.addPage(cur_pg)
        print(str(ii) + "导入文件")
    with open(out_path, 'wb') as f:
        out_pdf.write(f)
    pass


def add_watermark(pdfs: str, water_mark: str, out_path: str = "", out_name='', suffix: str = "_out",
                  auto_adjust=True,
                  rot_deg=0, dx=0, dy=0,
                  ):
    """
    :param pdfs: 原文件,可含有多个文件
    :param water_mark: 水印文件, 仅读取第一个文件
    :param out_path: 输出路径, 可为空
    :param out_name: 输出文件名称, 可为空
    :param suffix: 后缀, 无后缀且同路径时将替换源文件
    :param auto_adjust: 是否自动调整位置, 默认Ture
    :param rot_deg: 转动
    :param dx: x平移
    :param dy: y平移
    :return: None
    """

    out_pdf = PdfFileWriter()
    dir, tmp = os.path.split(pdfs)
    ext = tmp.split('.')[-1]
    filename = tmp.replace('.%s' % ext, '')
    if out_name == "":
        out_name = filename
    else:
        out_name = out_name.split('.')[0]

    if out_path == "":
        out_path = os.path.join(dir, out_name + ".pdf")
    else:
        out_path = os.path.join(out_path, out_name + ".pdf")

    wm = PdfFileReader(open(water_mark, 'rb'), strict=False).getPage(0)
    wm_w, wm_h = wm['/MediaBox'][2:]
    kk = 1

    src_pdf = PdfFileReader(open(pdfs, 'rb'), strict=False)

    for pg in src_pdf.pages:
        cur_pg = pg
        cur_pg_w, cur_pg_h = cur_pg['/MediaBox'][2:]
        if not auto_adjust:
            rotation = math.radians(rot_deg)
            MatrixA = [math.cos(rotation), math.sin(rotation),
                       -math.sin(rotation), math.cos(rotation),
                       dx, dy]
        else:  # 自动调整
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
        out_pdf.addPage(cur_pg)

    with open(out_path, 'wb') as f:
        out_pdf.write(f)

    pass


class Merger():
    Name = ""
    RootDir = ""
    FileName = ''

    def __init__(self, rootPath):
        self.Name = os.path.basename(rootPath)
        self.Name = self.Name.upper()
        self.FileName = self.Name + ".pdf"
        for root, dirs, files in os.walk(rootPath):
            self.FrontMaters = files
            self.SavePath = os.path.join(os.getcwd(), self.FileName)
            self.RootDir = rootPath
            break
        return

    def add_pages(self, pdfWriter, pdfReader):
        for i in range(pdfReader.numPages):
            self.add_pages(pdfWriter, pdfReader.getPage(i))
        pass

    def add_page(self, pdfWriter, page):
        try:
            if page.bleedBox.getHeight() > page.bleedBox.getWidth():
                if list(page.keys()).__contains__("/Rotate"):
                    if page["/Rotate"] == 0:
                        page.rotateClockwise(270)
                else:
                    page.rotateClockwise(270)
            pdfWriter.addPage(page)
            return 0
        except:
            print("%s add fail!" % page.pdf.stream.name)
            return -1
        finally:
            pass

    @staticmethod
    def get_drawing_no(FileName):
        return FileName.split(' ')[0]

    def merge(self, SavePath=""):
        if SavePath != "":
            self.SavePath = SavePath
        pdf_writer = PdfFileWriter()
        for frt in self.FrontMaters:
            pdf_reader = PdfFileReader(open(os.path.join(self.RootDir, frt), 'rb'), strict=False)
            self.add_pages(pdf_writer, pdf_reader)
            # pdf_writer.addBookmark(frt.split(' ')[0], pdf_writer.getNumPages()-pdf_reader.getNumPages(), bold=True)

        with open(self.SavePath, 'wb') as f:
            pdf_writer.write(f)

        pass
