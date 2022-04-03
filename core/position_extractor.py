#!/root/anaconda3/bin/python
import os
import re 
import pdfplumber as pb
import pandas as pd

def __find_files(file_dir):
    """迭代查找文件"""
    file_paths = []
    for root, _, files in os.walk(file_dir):
        for file in files:
            path = os.path.join(root, file)
            rear = os.path.splitext(path)[1]
            if rear in [".doc", ".docx", ".pdf"]:
                file_paths.append(path)
    return file_paths

def __extract_text(path):
    """
    抽取文本内容
    """
    text = ""
    try:
        if os.path.splitext(path)[1] == ".pdf":
            pdf = pb.open(path)
            for page in pdf.pages:
                
                text += page.extract_text() if page.extract_text() else ""
    except Exception as e:
        print(path,e)
    return text


def position_extract(path):

    if re.search(r"【.*?】",path):
        position = re.findall(r"【.*?】", path)
        if len(position)>0:
            position = position[0]
            return re.search(r'[a-zA-Z\u4e00-\u9fa5]+',position).group()
    
    if re.search(r"[\u4e00-\u9fa5]*？[-_].+[ -_]",path):
        position = re.findall(r"[-_].+[ -_]", path)[0]
        position = position.split("-")[1]
        return re.search(r'[a-zA-Z\u4e00-\u9fa5]+',position).group()
    return ''

# if __name__ == '__main__':
    
#     path = r'..\docs\长亮金服招聘团队简历'
#     files = __find_files(path)
    
#     files = [os.path.splitext(i)[0] + '.pdf' if os.path.splitext(i)[1] in ['.doc','.docx'] else i for i in files]
#     files = [os.path.abspath(i) for i in files]
#     files = list(set(files))

#     df = pd.DataFrame(columns = ['filename','position'])

#     for i in files:
#         filename = os.path.basename(i)
#         res = position_extract(filename)
#         df = df.append({'filename': i,'position':res},ignore_index = True)
            
    # df.to_csv(r'.\tests\test_position.csv',encoding = 'utf-8-sig',index = False)