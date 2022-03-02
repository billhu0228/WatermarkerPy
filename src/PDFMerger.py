import math
import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from PyPDF2.generic import Bookmark
from PyPDF2.pdf import PageObject
from Functions import create_watermark


def SearchFile(path, ext):
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            for k in SearchFile(os.path.join(path, item), ext):
                yield k
        else:
            if item.endswith(ext):
                yield os.path.join(path, item)


# def RotatePage(page: PageObject):
#     if page.bleedBox.getHeight() > page.bleedBox.getWidth():
#         if list(page.keys()).__contains__("/Rotate"):
#             if page["/Rotate"] == 0:
#                 page.rotateClockwise(270)
#             # else:
#             #     page.rotateClockwise(270)
#     return page

def AddWaterMarkerByPage(page: PageObject, water_mark: PageObject,
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


def AddWaterMarkerByList(pdfs: str, page_dict, water_mark: str, out_path: str = "", out_name='', suffix: str = "_out",
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
    pages_to_add=page_dict.keys()
    for ii, pg in enumerate(src_pdf.pages):
        cur_pg = pg
        if ii in pages_to_add:
            create_watermark(page_dict[ii])
            print(page_dict[ii]+"水印生成")
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
            print(page_dict[ii]+"水印添加")
        else:
            pass
        out_pdf.addPage(cur_pg)
        print(str(ii) + "导入文件")
    with open(out_path, 'wb') as f:
        out_pdf.write(f)
    pass


def AddWaterMarker(pdfs: str, water_mark: str, out_path: str = "", out_name='', suffix: str = "_out",
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

    def AddPages(self, pdfWriter, pdfReader):
        for i in range(pdfReader.numPages):
            self.AddPage(pdfWriter, pdfReader.getPage(i))
        pass

    def AddPage(self, pdfWriter, page):
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

    @staticmethod
    def GetDrawingNo(FileName):
        return FileName.split(' ')[0]

    def merge(self, SavePath=""):
        if SavePath != "":
            self.SavePath = SavePath
        pdf_writer = PdfFileWriter()
        for frt in self.FrontMaters:
            pdf_reader = PdfFileReader(open(os.path.join(self.RootDir, frt), 'rb'), strict=False)
            self.AddPages(pdf_writer, pdf_reader)
            # pdf_writer.addBookmark(frt.split(' ')[0], pdf_writer.getNumPages()-pdf_reader.getNumPages(), bold=True)

        with open(self.SavePath, 'wb') as f:
            pdf_writer.write(f)

        pass
