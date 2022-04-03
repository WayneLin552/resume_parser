import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import easyocr
import fitz
# import cv2 as cv
# from pdf2image import convert_from_path

reader = easyocr.Reader(['ch_sim','en'])

def OCR_text(pdfPath,imagePath):    
    # print("imagePath="+imagePath)
    pdfDoc = fitz.open(pdfPath)
    text = ''
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72 我扫描的文件是200dpi
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        zoom_x = 1.3                  #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.3
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        # print(pix)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix.writePNG(imagePath+'/'+'images_%s.png' % (pg+1))   # 将图片写入指定的文件夹内
        result = reader.readtext(imagePath+'/'+'images_%s.png' % (pg+1))
        for i in result:
            text += '-'+i[1] if i[1] else ' '
        os.remove(imagePath+'/'+'images_%s.png' % (pg+1))
    return text

if __name__=='__main__':
    text = OCR_text(r'C:\Users\Wayne\Desktop\docword\长亮金服-前端开发-谭国斌.pdf',r'C:\Users\Wayne\Desktop\docword\pic_temp')
    text