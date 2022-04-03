#!/root/anaconda3/bin/python
import os
import re
import pdfplumber as pb
import pandas as pd

# set去重
__school_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/school_dic", 'r',encoding = 'utf-8')])

__school_list = list(__school_set)

# 去除空行
__school_list = [i for i in __school_list if i != '']

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

def school_extract(text):
    """学校名称"""
    college = []
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)]
   
    # 先在前10行找
    for i in lines:#range(min(20,len(lines))):
        # 先通过"学校名称"字段去查找”
        tmp1 = re.search(r"(学校名称|毕业学校|毕业院校)[:：\s\n]*?[\u4e00-\u9fa5]{4,12}", i)
        if tmp1:
            college.append(re.findall(r"(学校名称|毕业学校|毕业院校)[:：\s\n]*?([\u4e00-\u9fa5]{4,12})", i)[0][1])
            return college[0]
        tmp2 = re.search(r"[\u4e00-\u9fa5]{2,10}(大学|学院|学校)", i)
        if tmp2:
            college.append(re.search(r"[\u4e00-\u9fa5]{2,10}(大学|学院|学校)", i).group())
            return college[0]
    return ''

    # if len(lines)<=10:
    #     return ''
    # else:    
    #     # print('else')
    #     for i in range(19,len(lines)):
    #         # print(lines[i])
    #         start_tag = re.search(r'教.{0,1}育.{0,1}背.{0,1}景|教.{0,1}育.{0,1}经.{0,1}历|教育背景',lines[i])   
    #         if start_tag:
    #             # print('find')
    #             # print(start_tag.group())
    #             # print(lines[i],start_tag.group())
    #             for j in range(i, len(lines)):
    #                 line_tmp = lines[j]
    #                 # print(line_tmp)
                    
    #                 # 控制停止搜索标识
    #                 end_tag = re.search(r'工\s*作|项\s*目|技\s*能|评\s*价|证\s*书|能\s*力',line_tmp)
    #                 if end_tag:
    #                     break
    #                 else:                                    
    #                     # 解析学校
    #                     school_tmp1 = re.search('|'.join(__school_list),line_tmp)
    #                     school_tmp2 = re.search(r'[\u4e00-\u9fa5]{2,10}(大学|学院|学校)',line_tmp)
    #                     if school_tmp2:
    #                         college.append(school_tmp2.group())
    #                         return college[0]                       
    #                     elif school_tmp1:
    #                         college.append(school_tmp1.group())  
    #                         return college[0]
    #     if len(college) >0:
    #         return college[0]
    #     else:
    #         return ''

if __name__ == "__main__":
    # path = r'..\docs\长亮金服简历\长亮- Java-魏源文.pdf'
    # text = __extract_text(path)
    # # print(text)
    # res = school_extract(text)
    # print(res)
    pass
    
    
    # path = r'..\docs\长亮金服简历'
    # files = __find_files(path)
    
    # # for i in files:
    # #     if os.path.splitext(i)[1] in ['.doc','.docx']:
    # #         __doc2pdf(os.path.abspath(i))
    
    # files = [os.path.splitext(i)[0] + '.pdf' if os.path.splitext(i)[1] in ['.doc','.docx'] else i for i in files]
    # files = [os.path.abspath(i) for i in files]
    # files = list(set(files))

    # df = pd.DataFrame(columns = ['filename','school'])

    # for i in files:
    #     text = __extract_text(i)
    #     res = school_extract(text)
    #     df = df.append({'filename': i,'school':res},ignore_index = True)
    
    # df['filename'] = df['filename'].apply(lambda x: x[x.rfind('\\') + 1:] if pd.notna(x) else '')    
        
    # df.to_csv(r'.\tests\test_school.csv',encoding = 'utf-8-sig',index = False)

