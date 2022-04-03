#!/root/anaconda3/bin/python
import os
import re 
import pdfplumber as pb
import pandas as pd
# from win32com.client import Dispatch


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


# def __doc2pdf(path):
    
#     word = Dispatch('Word.Application')
#     doc = word.Documents.Open(path)
#     new_path = os.path.splitext(path)[0] + '.pdf'
#     doc.SaveAs(new_path, FileFormat=17) # wdFormatPDF
#     doc.Close()
#     word.Quit()
    
    
def skills_extract(text):
    skills = ''  
    
    lines = text.split('\n') 
    #print(lines)
    for i in range(len(lines)):
        # 控制识别开始标识
        start_tag = re.search(r'专\s*业\s*技\s*能|相\s*关\s*技\s*能|技\s*能\s*专\s*长|技\s*术\s*优\s*势|职\s*业\s*能\s*力|专\s*业\s*技\s*术|掌\s*握\s*技\s*能|个\s*人\s*技\s*能|职\s*业\s*技\s*能|掌\s*握\s*技\s*能|I\s*T\s*技\s*能|专\s* 项\s*技\s*能|个\s*人\s*优\s*势|技\s*能\s*特\s*长|主\s*要\s*特\s*长',lines[i])
            
        if start_tag:
            # print(lines[i],start_tag.group())
            for j in range(i + 1, len(lines)):
                line_tmp = lines[j]
                
                # 控制停止搜索标识
                end_tag = re.search(r'项\s*目\s*经\s*验|项\s*目\s*经\s*历|近\s*期\s*工\s*作|.\s*作\s*经\s*验|.\s*作\s*经\s*历|自\s*我\s*推\s*荐|自\s*我\s*评\s*|工\s作\s经|证\s*书|在\s*校|意\s*向|求\s*职\s*意\s*向|自\s*我\s*描\s*述|校\s*园\s*经\s*历|工\s*作\s*内\s*容|毕\s*业|.\s*作\s*背\s*景|职\s*业\s*培\s*训|教\s*育\s*背\s*景|教\s*育\s*经\s*历|人\s*生\s*态\s*度|证\s*书|荣\s*誉\s*奖\s*项',line_tmp)
                if end_tag:
                    break
                else:
                    skills += line_tmp
                    
            break              
        else:
           continue    
    
    return skills



if __name__ == '__main__':
        
    # files = r'..\docs\长亮金服招聘团队简历\boss直聘-吴彤\Boss直聘-吴彤\【测试工程师_北京】宋肖肖 4年.pdf'

    # df = pd.DataFrame(columns = ['filename','date','school','major','degree'])
    
    # res = education_experience_extractor(files)

    # df = df.append({'filename':res['filename'],'date':res['date'],\
    #             'school':res['school'],'major':res['major'],\
    #                 'degree':res['degree']},ignore_index = True)
    
    path = r'..\docs\长亮金服招聘团队简历'
    files = __find_files(path)
    
    # for i in files:
    #     if os.path.splitext(i)[1] in ['.doc','.docx']:
    #         __doc2pdf(os.path.abspath(i))
    
    files = [os.path.splitext(i)[0] + '.pdf' if os.path.splitext(i)[1] in ['.doc','.docx'] else i for i in files]
    files = [os.path.abspath(i) for i in files]
    files = list(set(files))
    files = [i.replace('F:\Job\长亮数据\研发项目\文本分析\resume_parser\docs\长亮金服招聘团队简历','') for i in files]
    df = pd.DataFrame(columns = ['filename','skills'])

    for i in files:
        text = __extract_text(i)
        res = skills_extract(text)
        df = df.append({'filename': i,'skills':res},ignore_index = True)
            
    df.to_csv(r'.\tests\test_skills.csv',encoding = 'utf-8-sig',index = False)
    
    print('END')
    
        
        
