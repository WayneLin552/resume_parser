#!/root/anaconda3/bin/python
import re
import os
# import pdfplumber
# import pandas as pd

# set去重 城市，职业
__city_list = list(set([v.strip() for v in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/city_dic", 'r',encoding = 'utf-8')]))
__job_list = list(set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/job_dic", 'r',encoding = 'utf-8')]))

# 去除空行
__city_list = [i for i in __city_list if i != '']
__job_list = [i for i in __job_list if i != '']


def name_extract(text,file):
    """
    获取姓名

    Parameters
    ----------
    text: string
        简历解析后的文本

    Returns: list
    -------
        姓名 / []
    """
    names = []
    
    # text = __extract_text(file)
    lines = [i for i in re.split(r'\n',text) if re.search(r'[\u4e00-\u9fa5]',i)] 
    
    # 先通过"姓名"字段去查找”
    # for line in lines:
    if re.search(r"姓\s*名[:：\s\n\t]*[\u4e00-\u9fa5]{2,4}", text):
        name = re.sub(r'姓\s*名[:：\s\n\t]*','',re.search(r"姓\s*名[:：\s\n\t]*([\u4e00-\u9fa5]{2,4})", text).group())
        names.append(name)
        # break       
    
    # 再没有在文件名中寻找
    if not names:              
        #print(file)
        filename_tmp = os.path.splitext(file)[0]
        filename = os.path.basename(filename_tmp)
        #print(filename)
        if '】' in filename or '【' in filename:
            filename_tmp = re.split('[【】]|\s+',filename)
        else:
            filename_tmp = re.split('[_—-]|\s+',filename)
        #print(filename_tmp)
        if filename_tmp:
            for i in filename_tmp:
                if i:
                    name_tmp = re.findall('^[\u4e00-\u9fa5]{2,4}$',i)
                    if name_tmp:
                        for j in name_tmp:
                            __city = ['^' + i + '$' for i in __city_list]
                            __job = ['^' + i + '$' for i in __job_list]
                            if not re.search(r'需求|高级|测试|运维|数据|应聘|招聘|长亮|简历|金融|科技|前端|后端|开发|工程师|意向|大专|专科|本科|硕士|博士',j)\
                                and not re.search('|'.join(__city),j) and not re.search('|'.join(__job),j):
                                names.append(i)
    
    # 没有的话提取第一个词
    if not names:
        # words = __extract_words(file)
        for line in lines:
            if not re.search(r"·~!@#$%^&*()_+`{}|\[\]\:\";\-\\\='<>?,./，。、《》？；：‘“{【】}|、！@#￥%……&*（）——+=-",line.replace(' ', ''))\
                and not re.search('需求|高级|应聘|简历|招聘|信息',line) and re.search(r'[\u4e00-\u9fa5]{2,4}',line):
               names.append(re.search(r'[\u4e00-\u9fa5]{2,4}',line).group())  
     
    if len(names) == 0:
        return ''
    else: return names[0]

if __name__ == "__main__":
    pass
    # path = r'..\docs\长亮金服简历'
    # print(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])
    
    # files = __find_files(path)
    
    # # for i in files:
    # #     if os.path.splitext(i)[1] in ['.doc','.docx']:
    # #         __doc2pdf(os.path.abspath(i))
    
    # files = [os.path.splitext(i)[0] + '.pdf' if os.path.splitext(i)[1] in ['.doc','.docx'] else i for i in files]
    # files = [os.path.abspath(i) for i in files]
    # files = list(set(files))

    # df = pd.DataFrame(columns = ['filename','name'])

    # for i in files:
    #     res = name_extract(i)
    #     df = df.append({'filename':os.path.basename(i),'name':res},ignore_index = True)
            
    # df.to_csv(r'.\tests\test_name2.csv',encoding = 'utf-8-sig',index = False)
    # print('END')