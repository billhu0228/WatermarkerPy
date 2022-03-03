# Python水印添加工具

--------------------------------------------------


### 简介

---------

使用几个已有的python包，实现的A3图纸添加水印、图号识别并增加字符等功能，供各位同事入门Python学习使用。同时也可以简化图纸签名、修改图号、修改图纸日期等常见功能，提高效率。



### 涉及的基础Python知识


----------

- 一个基于PyCharm的Python项目结构；
- 的第三方 **Packages** 和 **Modules** 的安装和导入；
- 自定义Modules的导入；
- 运行和调试；
- 函数和类的定义；
- 相对路径；
- PDF格式的基础概念；

### 安装必要的Package

------------

在命令行中使用如下命令安装名为 “xxx” 的Package:

    pip install xxx

本项目需要安装的Package包括：

- PyPDF2
- reportlab
- Wand
- numpy
- Pillow
- pytesseract

### 安装必要的程序

------------------------

- **[Ghostscript](https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs9550/gs9550w32.exe)**

用于图像处理

- **[tesseract](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.1.20220118.exe)**

图像识别

- **[ImageMagick](https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.1.0-26-Q16-HDRI-x64-dll.exe)**

图片相关功能



### 两个示例项目

-----------

#### YN项目日期和签名水印

YN项目竣工图水印需要把已经制作好的水印文件叠加到已有图纸上，添加人员签名，并修改日期。


#### KNY项目竣工图水印

KNY项目竣工图水印工作需要识别图册中哪些页面带有图框，对于又图框的页面，需要识别图号，并根据原图号生成一个新图号（原图号后加字符  'J'）的水印，加盖于原图号位置，实现方式分解为**4**步：

1. 判断是否是图号位置：判断局部区域是否存在颜色，**Wand** 包；
2. 文字识别：图像识别包 **pytesseract**；
3. 生成图号水印文件：pdf生成包 **reportlab**；
4. 水印叠加：**PyPDF2** 包；



### 部分函数功能

---------

- 添加水印


```python
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
```

- 计算一个区域的平均蓝

```python
def average_blue(img: 'Image', x0: int, y0: int, w: int, h: int) -> float:
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
```

- 文本识别

```python
ret = cut(img, 1660, 1290, 270, 25)
s = pytesseract.image_to_string(ret, config=tesseract_config)
```
