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
- 





Install latest development version with pip from GitHub:

- The `drawing` add-on is a translation layer to send DXF data to a render backend, interfaces to 
  [matplotlib](https://pypi.org/project/matplotlib/), which can export images as png, pdf or svg, 
  and [PyQt5](https://pypi.org/project/PyQt5/) are implemented.
- `r12writer` add-on to write basic DXF entities direct and fast into a DXF R12 file or stream
- `iterdxf` add-on to iterate over DXF entities of the modelspace of really big (> 5GB) DXF files which
  do not fit into memory
- `Importer` add-on to import entities, blocks and table entries from another DXF document
- `dxf2code` add-on to generate Python code for DXF structures loaded from DXF 
  documents as starting point for parametric DXF entity creation
- Plot Style Files (CTB/STB) read/write add-on

A simple example:

```python
import ezdxf

# Create a new DXF document.
doc = ezdxf.new(dxfversion='R2010')

# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.new('TEXTLAYER', dxfattribs={'color': 2})

# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace, 
# paperspace layout or block definition).  
msp = doc.modelspace()

# Add entities to a layout by factory methods: layout.add_...() 
msp.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
msp.add_text(
    'Test', 
    dxfattribs={
        'layer': 'TEXTLAYER'
    }).set_pos((0, 0.2), align='CENTER')

# Save DXF document.
doc.saveas('test.dxf')
```

Example for the *r12writer*, which writes a simple DXF R12 file without in-memory structures:

```python
from random import random
from ezdxf.addons import r12writer

MAX_X_COORD = 1000
MAX_Y_COORD = 1000

with r12writer("many_circles.dxf") as doc:
    for _ in range(100000):
        doc.add_circle((MAX_X_COORD*random(), MAX_Y_COORD*random()), radius=2)
```

The r12writer supports only the ENTITIES section of a DXF R12 drawing, no HEADER, TABLES or BLOCKS section is
present, except FIXED-TABLES are written, than some additional predefined text styles and line types are available.

安装依赖程序
------------

Install with pip for Python 3.6 and later:

    pip install ezdxf

Install latest development version with pip from GitHub:

    pip install git+https://github.com/mozman/ezdxf.git@master

or from source:

    python setup.py install

Website
-------

https://ezdxf.mozman.at/

Documentation
-------------

Documentation of development version at https://ezdxf.mozman.at/docs

Documentation of latest release at http://ezdxf.readthedocs.io/

Contribution
------------

The source code of *ezdxf* can be found at __GitHub__, target your pull requests to the `master` branch:

http://github.com/mozman/ezdxf.git


Feedback
--------

Questions and feedback at __Google Groups__:

https://groups.google.com/d/forum/python-ezdxf

python-ezdxf@googlegroups.com

Questions at __Stack Overflow__:

Post questions at [stack overflow](https://stackoverflow.com/) and use the tag `dxf` or `ezdxf`.

Issue tracker at __GitHub__:

http://github.com/mozman/ezdxf/issues

Contact
-------

Please post questions at the [forum](https://groups.google.com/d/forum/python-ezdxf) or 
[stack overflow](https://stackoverflow.com/) to make answers available to other users as well.

ezdxf@mozman.at

Feedback is greatly appreciated.

Manfred



安装必要的程序：

**[Ghostscript](https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs9550/gs9550w32.exe)**、**[tesseract](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.1.20220118.exe)**、**[ImageMagick](https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.1.0-26-Q16-HDRI-x64-dll.exe)**





