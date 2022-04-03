#!/root/anaconda3/bin/python
# -*- coding: utf-8 -*-
import os
import re 
import pdfplumber
import pandas as pd
# from win32com.client import Dispatch

# set去重
__major_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/major_dic", 'r',encoding = 'utf-8')])
__school_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/school_dic", 'r',encoding = 'utf-8')])

__major_list = list(__major_set)
__school_list = list(__school_set)

# 去除空行
__major_list = [i for i in __major_list if i != '']
__school_list = [i for i in __school_list if i != '']



def find_files(file_dir):
    """迭代查找文件"""
    file_paths = []
    file_names = []
    for root, _, files in os.walk(file_dir):
        for file in files:
            path = os.path.join(root,file)
            rear = os.path.splitext(path)[1]
            if rear in [".pdf"]: #本处只考虑pdf
                file_paths.append(path)
                file_names.append(file)
    return file_paths, file_names

def __extract_text(path):
    """
    抽取文本内容
    """
    text = ""
    try:
        if os.path.splitext(path)[1] == ".pdf":
            pdf = pdfplumber.open(path)
            for page in pdf.pages:
                
                text += page.extract_text() if page.extract_text() else ""
    except Exception as e:
        print(path,e)
    return text


# def __doc2docx(path):
    
#     word = Dispatch('Word.Application')
#     doc = word.Documents.Open(path)
#     new_path = os.path.splitext(path)[0] + '.docx'
#     doc.SaveAs(new_path, FileFormat=17) # wdFormatPDF
#     doc.Close()
#     word.Quit()
    
    
def education_experience_extract_data(text):
    edu_exp = {}
    edu_exp['edu_start_date'] = []
    edu_exp['edu_end_date'] = []
    edu_exp['edu_school'] = []
    edu_exp['edu_major'] = []
    edu_exp['edu_degree'] = []    
    tempmajor_list = []
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)] 
    
    # lines = re.split(r',|，|。|\t',text)
    #print(lines)
    for i in range(len(lines)):
        start_tag = re.search(r'教\s*育\s*背\s*景|教\s*育\s*经\s*历|学\s*习\s*经\s*历',lines[i])
            
        if start_tag:
            flag = False
            mode = 0
            # print(lines[i],start_tag.group())
            for j in range(i, len(lines)):
                line_tmp = lines[j]
                
                # 控制停止搜索标识
                end_tag = re.search(r'工\s*作|项\s*目|技\s*能|评\s*价|证\s*书|能\s*力|实\s*习',line_tmp)
                if end_tag:
                    break
                else:                 
                    # if re.search(r'专\s*业\s*描\s*述',line_tmp):
                    #     continue
                    if len(edu_exp['edu_school'])==0 and len(tempmajor_list)>0:
                        #说明先专业后学校
                        mode = 1
                        #否则先学校后专业 mode=1
                    # 解析日期
                    date_tmp1 = re.search(r'20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|现在|20\d{2}[\s年—－–\-~～/.\\]+.今)',line_tmp)               
                    date_tmp2 = re.search(r'20\d{2}[\s到至年—－–\-~～/.\\]+(20\d{2}[\s年]*|.今|现在)',line_tmp)   
                    date_tmp3 = re.search(r'20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月—－–\-~～/.\\]+\d{1,2}[\s日]*[\s到至—－–\-~～/.\\]*(20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月—－–\-~～/.\\]+\d{1,2}[\s日]*|.今|现在)',line_tmp)
                    # date_tmp = re.search(r'[0-9]{4}[\s\d年至月—\-~～/.\\]*[\s至年月—\-~～/.\\]*[\s\d年至月—\-~～/.\\]*([\d月年]+|至今)',line_tmp)
                    # if date_tmp:
                    #     print('date_tmp',date_tmp.group())
                    
                    if date_tmp1:
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp1.group()) if re.search(r'\d|今',i)]
                        if len(time)>3:
                            edu_exp['edu_start_date'].append('{}.{}'.format(time[0], time[1]))
                            edu_exp['edu_end_date'].append('{}.{}'.format(time[2], time[3]))
                        elif len(time)==3:                           
                            edu_exp['edu_start_date'].append('{}.{}'.format(time[0], time[1]))
                            edu_exp['edu_end_date'].append('{}'.format(time[2]))
                    elif date_tmp2:
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp2.group()) if re.search(r'\d|今',i)]
                        if len(time)==2:
                            edu_exp['edu_start_date'].append('{}'.format(time[0]))
                            edu_exp['edu_end_date'].append('{}'.format(time[1]))
                    elif date_tmp3:
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp3.group()) if re.search(r'\d|今',i)]
                        if len(time)>4:
                            edu_exp['edu_start_date'].append('{}.{}.{}'.format(time[0], time[1], time[2]))
                            edu_exp['edu_end_date'].append('{}.{}.{}'.format(time[3], time[4], time[5]))
                        elif len(time)==4:                           
                            edu_exp['edu_start_date'].append('{}.{}.{}'.format(time[0], time[1], time[2]))
                            edu_exp['edu_end_date'].append('{}'.format(time[3]))
                    
                    # 解析学校
                    school_tmp2 = re.search('|'.join(__school_list),line_tmp)
                    school_tmp1 = re.search(r'[\u4e00-\u9fa5]+(大学|学院|学校)',line_tmp)
                    
                    if school_tmp1:
                        edu_exp['edu_school'].append(school_tmp1.group())
                        flag = True
                        # tempschool_list.append(school_tmp.group())
                        if flag == True and mode == 1: #先专业后学校
                            edu_exp['edu_major'].append(tempmajor_list[-1])
                            tempmajor_list.pop()
                            flag = False
                        line_tmp = line_tmp.lstrip(school_tmp1.group())
                                               
                    elif school_tmp2:
                        edu_exp['edu_school'].append(school_tmp2.group())
                        flag = True
                        if flag == True and mode == 1: #先专业后学校
                            edu_exp['edu_major'].append(tempmajor_list[-1])
                            tempmajor_list.pop()
                            flag = False
                        line_tmp = line_tmp.lstrip(school_tmp2.group())                   
                    
                    # 解析专业                          
                    major_tmp = re.search('|'.join(__major_list),line_tmp)
                    if major_tmp:
                        tempmajor_list.append(major_tmp.group())
                        if flag == True and mode == 0: #先学校后专业
                            edu_exp['edu_major'].append(tempmajor_list[-1])
                            tempmajor_list.pop()
                            flag = False                                            
                    
                    # 解析学历
                    degree_tmp = re.search(r'初\s*中|高\s*中|职\s*高|中\s*专|专\s*科|\
                                           技\s*校|大\s*专|本\s*科|硕\s*士\s*研\s*究\s*生|\
                                               在\s*职\s*研\s*究\s*生|工\s*程\s*硕\s*士|\
                                               专\s*业\s*硕\s*士|博\s*士\s*研\s*究\s*生|\
                                                   博\s*士\s*在\s*读|M\s*B\s*A\s*硕士|\
                                                       M\s*B\s*A|E\s*M\s*B\s*A|\
                                                           工\s*商\s*管\s*理\s*硕\s*士|\
                                                               工\s*学\s*学\s*士|访\s*问\s*学\s*者|\
                                                                   博\s*士\s*后|研\s*究\s*生|\
                                                                       硕\s*士|博\s*士|学\s*士',line_tmp)
                                                    
                    if degree_tmp:
                        edu_exp['edu_degree'].append(degree_tmp.group())
                    
            break              
        else:
           continue    
    
    return edu_exp

def education_experience_extract(text):
    # data_list = []
    data = education_experience_extract_data(text)
    maxlength = max(len(data['edu_school']),len(data['edu_start_date']),len(data['edu_end_date']),len(data['edu_major']),len(data['edu_degree']))
    data['edu_school'].extend(' '*(maxlength-len(data['edu_school'])))
    data['edu_start_date'].extend(' '*(maxlength-len(data['edu_start_date'])))
    data['edu_end_date'].extend(' '*(maxlength-len(data['edu_end_date'])))
    data['edu_major'].extend(' '*(maxlength-len(data['edu_major'])))
    data['edu_degree'].extend(' '*(maxlength-len(data['edu_degree'])))
    data_tmp = sorted(list(zip(data['edu_school'],data['edu_start_date'],data['edu_end_date'],data['edu_major'],data['edu_degree'])),key=lambda x:x[1],reverse=True)
    return data_tmp
    # for i in range(len(data_tmp)):
    #     dic = {}
    #     dic['学校名称'] = data_tmp[i][0]
    #     dic['起止时间'] = data_tmp[i][1]
    #     dic['所学专业'] = data_tmp[i][2]
    #     dic['学位'] = data_tmp[i][3]
    #     data_list.append(dic)
    # if len(data_list)==0:
    #     return ''
    # else: return data_list


if __name__ == '__main__':        
    
    path = r'C:\Users\Wayne\Desktop\长亮科技\简历解析项目\gittest\长亮金服简历20220214'
    files,names = find_files(path)
    
    # for i in files:
    #     if os.path.splitext(i)[1] in ['.doc','.docx']:
    #         __doc2pdf(os.path.abspath(i))
    
    df = pd.DataFrame(columns = ['filename','edu_date','edu_school','edu_major','edu_degree'])

    for i,name in zip(files[:20],names[:20]):
        # print(name)
        text = __extract_text(i)
        res = education_experience_extract(text)
        print(res,name)
    #     df = df.append({'filename': i,'edu_date':res['edu_date'],\
    #                 'edu_school':res['edu_school'],'edu_major':res['edu_major'],\
    #                     'edu_degree':res['edu_degree']},ignore_index = True)
            
    # df.to_csv(r'test_edu.csv',encoding = 'utf-8-sig',index = False)
    
        
        
