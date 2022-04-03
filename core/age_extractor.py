#!/root/anaconda3/bin/python
# -*- coding: utf-8 -*-
import re
import os
import pdfplumber as pb
import datetime
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
    print(text)
    return text

def age_extract(text):
    #搜索年龄
    
    #年龄词语定位 
    if re.search(r"年\s*龄",text):
        tmp2 = re.findall(r"年\s*龄[:：：\s\n]*?(\d{2})",text,re.DOTALL)
        if tmp2:
            if 16 <= float(tmp2[0]) <= 70:
                return float(tmp2[0])
        #出生日期定位
    elif re.search(r"出生|生日",text):
        tmp3 = re.search(r"出生.*?[0-9]{4}|生日.*?[0-9]{4}",text,re.DOTALL)
        if tmp3:
            if 16 <= float(datetime.date.today().year - int(re.search(r'\d{4}',tmp3.group()).group())) <= 70:
                return float(datetime.date.today().year - int(re.search(r'\d{4}',tmp3.group()).group()))
        # 生日定位
    # elif re.search(r"",text):
    #     tmp4 = re.findall(r"",text)
    #     if tmp4:
    #         if 16 <= float(datetime.date.today().year - int(tmp4[0])) <= 70:
    #             return float(datetime.date.today().year - int(tmp4[0]))
    
    for i in text.split("\n"): 
        #x岁定位
        tmp1 = re.findall(r"(\d{2})\s*岁",i)
        if tmp1:
            # print(tmp1)
            if 16 <= float(tmp1[0]) <= 70:
                return float(tmp1[0])       

    return ''


if __name__ == "__main__":
    # files = r'..\docs\长亮金服简历\【数据分析_深圳】刘斌.pdf'

    # df = pd.DataFrame(columns = ['filename','date','school','major','degree'])
    # text = __extract_text(files)
    
    # res = age_extract(text)

    # df = df.append({'filename':res['filename'],'date':res['date'],\
    #             'school':res['school'],'major':res['major'],\
    #                 'degree':res['degree']},ignore_index = True)
    print(1)
    
    pass
    
    
    # path = r'..\docs\长亮金服简历'
    # files = __find_files(path)
    
    # # for i in files:
    # #     if os.path.splitext(i)[1] in ['.doc','.docx']:
    # #         __doc2pdf(os.path.abspath(i))
    
    # files = [os.path.splitext(i)[0] + '.pdf' if os.path.splitext(i)[1] in ['.doc','.docx'] else i for i in files]
    # files = [os.path.abspath(i) for i in files]
    # files = list(set(files))

    # df = pd.DataFrame(columns = ['filename','age'])

    # for i in files:
    #     text = __extract_text(i)
    #     res = age_extract(text)
    #     df = df.append({'filename': i,'age':res},ignore_index = True)
    
    # df['filename'] = df['filename'].apply(lambda x: x[x.rfind('\\') + 1:] if pd.notna(x) else '')    
        
    # df.to_csv(r'.\tests\test_age.csv',encoding = 'utf-8-sig',index = False)