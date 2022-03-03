from src.functions import *

if __name__ == "__main__":
    input_dir = "./input/yn"
    out_path = "./output/YN输出/"
    wmark_file = "./data/mark2.pdf"
    for file in os.listdir(input_dir):
        input_pdf = os.path.join(input_dir, file)
        out_filename = os.path.join(out_path, file + "_J.pdf")
        out_pdf = PdfFileWriter()
        src_pdf = PdfFileReader(open(input_pdf, 'rb'), strict=False)
        num_page = len(src_pdf.pages)
        for i, pg in enumerate(src_pdf.pages):
            cur_pg = pg
            dst_pdf = PdfFileWriter()
            dst_pdf.addPage(cur_pg)
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
            print("页面 %i / %i 输出.." % (i, num_page))
        with open(out_filename, 'wb') as f:
            out_pdf.write(f)
