from wand.image import Image

from PIL import Image as PImage
import numpy as np
import re

import io

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def cut(img: 'Image', x0: int, y0: int, w: int, h: int):
    ret = img.clone()[x0:x0 + w, y0:y0 + h]
    img_buffer = np.asarray(bytearray(ret.make_blob(format='png')), dtype='uint8')
    bytesio = io.BytesIO(img_buffer)
    pil_img = PImage.open(bytesio)
    return pil_img

def correct_no_RF(s: str):
    # if i==72:
    #     return "NEP/CD/SEC1/BR/SGR01/240001J"
    # elif i == 73:
    #     return "NEP/CD/SEC1/BR/SGR01/240002J"
    s=s.strip()
    if s.__contains__('-'):
        s=s[0:-2]
    if "BR" in s:
        tmp=re.split("BR",s)
    else:
        raise Exception("错误：%s" % s)
    news="NEP/CD/RFD"+"/BR/"+tmp[-1][1:]
    news+="J"
    return news


def correct_no(s: str,secn,i=0):
    # if i==72:
    #     return "NEP/CD/SEC1/BR/SGR01/240001J"
    # elif i == 73:
    #     return "NEP/CD/SEC1/BR/SGR01/240002J"
    s=s.strip()
    if s.__contains__('-'):
        s=s[0:-2]
    if "BR" in s:
        tmp=re.split("BR",s)
    else:
        raise Exception("错误：%s" % s)
    news="NEP/CD/SEC"+secn+"/BR/"+tmp[-1][1:]
    news+="J"
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
