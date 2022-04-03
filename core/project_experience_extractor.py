#!/root/anaconda3/bin/python

import os
import pdfplumber as pb
import pandas as pd
import re

# set去重
__job_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/job_dic", 'r',encoding = 'utf-8')])
__job_list = list(__job_set)

# 去除空行
__job_list = [i for i in __job_list if i != '']


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
        with pb.open(path) as pdf:
            for page in pdf.pages:                
                text += page.extract_text() if page.extract_text() else ""
    except Exception as e:
        print(path,e)
    return text

def project_experience_extract_data(text):
    
    """
    项目经历-项目名称
    项目经历-起止时间
    项目经历-项目角色
    项目经历-项目描述
    """
    proj_exp = {}
    proj_exp['proj_name'] = []
    proj_exp['proj_start_date'] = []
    proj_exp['proj_end_date'] = []
    proj_exp['proj_role'] = []
    proj_exp['proj_desc'] = []  
    temp_list1 = ''
    temp_list2 = ''
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)]  
    for i in range(len(lines)):
        start_tag = re.search(r'目[^的]{0,1}经.{0,1}历|目[^的]{0,1}经.{0,1}验|项\s目\s经|项\s*.\s*背\s*景|项.*目[^的]*经.*历|项.*目[^的]*信.*息|项\s*目\s*一',lines[i])
            
        if start_tag:
            flag1 = False #直接插旗用排除法来一行行加入项目角色
            flag2 = False #直接插旗用排除法来一行行加入项目描述
            for j in range(i, len(lines)):
                line_tmp = lines[j]
                # flag = True
                # 控制停止搜索标识 教\s*育|电\s*话|手\s*机|邮\s*箱|性\s*别|籍\s*贯|学\s*历|年\s*龄|QQ|
                end_tag = re.search(r'近\s*期\s*工\s*作|.\s*作\s*经\s*验|.\s*作\s*经\s*历|自\s*我\s*推\s*荐|自\s*我\s*评\s*|工\s作\s经|专\s*业\s*技\s*能|相\s*关\s*技\s*能|证\s*书|在\s*校|意\s*向|求\s*职\s*意\s*向|自\s*我\s*描\s*述|校\s*园\s*经\s*历|工\s*作\s*内\s*容|毕\s*业|.\s*作\s*背\s*景|职\s*业\s*培\s*训|教\s*育\s*背\s*景|教\s*育\s*经\s*历|人\s*生\s*态\s*度|证\s*书|荣\s*誉\s*奖\s*项',line_tmp)
                if end_tag:
                    proj_exp['proj_role'].append(temp_list1)                    
                    temp_list1 = ''
                    proj_exp['proj_role'] = [i for i in proj_exp['proj_role'] if i!='']
                    proj_exp['proj_desc'].append(temp_list2) 
                    temp_list2 = ''
                    proj_exp['proj_desc'] = [i for i in proj_exp['proj_desc'] if i!='']
                    return proj_exp
                elif j==len(lines)-1:
                    proj_exp['proj_role'].append(temp_list1)                    
                    temp_list1 = ''
                    proj_exp['proj_role'] = [i for i in proj_exp['proj_role'] if i!='']
                    proj_exp['proj_desc'].append(temp_list2) 
                    temp_list2 = ''
                    proj_exp['proj_desc'] = [i for i in proj_exp['proj_desc'] if i!='']
                    return proj_exp
                else:
                    if flag2 == False:                        
                        proj_exp['proj_desc'].append(temp_list2) 
                        temp_list2 = ''
                    if flag1 == False:
                        proj_exp['proj_role'].append(temp_list1) 
                        temp_list1 = ''
                    
                    # 解析日期
                    date_tmp1 = re.search(r'20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|20\d{2}[\s年—－–\-~～/.\\]+.今)',line_tmp)
                    # date_tmp2 = re.search(r'20\d{2}[\s年—–\-~～/.\\]+\d{1,2}[\s月—–\-~～/.\\]+\d{1,2}[\s日]*[\s到至—–\-~～/.\\]*(20\d{2}[\s年—–\-~～/.\\]+\d{1,2}[\s月—–\-~～/.\\]+\d{1,2}[\s日]*|.今)',line_tmp)
                    date_tmp2 = re.search(r'20\d{2}[\s年—－–\-~～/.\\]+\d{1,2}[\s月—－–\-~～/.\\]*',line_tmp)
                    
                    if date_tmp1:
                        flag1 = False
                        flag2 = False
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp1.group()) if re.search(r'\d|今',i)]
                        if len(time)>3:
                            proj_exp['proj_start_date'].append('{}.{}'.format(time[0], time[1]))
                            proj_exp['proj_end_date'].append('{}.{}'.format(time[2], time[3]))
                        elif len(time)==3:                           
                            proj_exp['proj_start_date'].append('{}.{}'.format(time[0], time[1]))
                            proj_exp['proj_end_date'].append('{}'.format(time[2]))
                        # proj_exp['proj_date'].append(date_tmp1.group()) #|商务公司|银行
                        try:
                            line_tmp = re.sub(date_tmp1.group(),'',line_tmp)
                        except:
                            continue
                    elif date_tmp2:
                        flag1 = False
                        flag2 = False
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp2.group()) if re.search(r'\d|今',i)]
                        if len(time)==2:
                            proj_exp['proj_start_date'].append('{}年{}月'.format(time[0], time[1]))
                            proj_exp['proj_end_date'].append('NULL')
                        # proj_exp['proj_date'].append(date_tmp2.group())
                        try:
                            line_tmp = re.sub(date_tmp2.group(),'',line_tmp)
                        except:
                            continue
                    # print('time',flag)
                    # 解析项目名
                    projname_tmp1 = re.search(r'项\s*目\s*(名\s*称|名\s*字|名)[一二三四五六七八九十1-9【】\[\]（）()\t\s:：–—\-~～/.\\]+[0-9A-Za-z\u4e00-\u9fa5\s]+',line_tmp)
                    projname_tmp2 = re.search(r'项\s*目\s*(一|二|三|四|五|六|七|八|九|十|[1-9]|１|２|３|４|：|:)[\t\s:：–—\-~～/.\\]+[0-9A-Za-z\u4e00-\u9fa5\s]+',line_tmp)
                    #通过时间的左右边查找
                    projname_tmp3 = re.search(r'[A-Za-z\u4e00-\u9fa5]+[^至今]*', line_tmp)
                    if projname_tmp3:
                       
                        projname_tmp3 = re.sub(r'至今','',projname_tmp3.group())
                        #projname_tmp3 = re.sub(r'今','',projname_tmp3.group())
                    
                    if projname_tmp1:
                        flag1 = False
                        flag2 = False
                        projname_tmp1 = re.sub(r'项\s*目\s*(名\s*称|名\s*字|名)[一二三四五六七八九十1-9【】\[\]（）()\t\s:：–—\-~～/.\\]+','',projname_tmp1.group()).replace(' ', '')
                        proj_exp['proj_name'].append(projname_tmp1)
                        try:
                            line_tmp = re.sub(projname_tmp1.group(),'',line_tmp)
                        except:
                            continue
                    elif projname_tmp2: 
                        flag1 = False
                        flag2 = False
                        projname_tmp2 = re.sub(r'项\s*目\s*(一|二|三|四|五|六|七|八|九|十|[1-9]|１|２|３|４|：|:)[\t\s:：–—\-~～/.\\]+','',projname_tmp2.group()).replace(' ', '')
                        proj_exp['proj_name'].append(projname_tmp2)
                        try:
                            line_tmp = re.sub(projname_tmp2.group(),'',line_tmp)
                        except:
                            continue
                    # 如果二者都没有，通过时间的左右方向查找
                    elif date_tmp1!=None and projname_tmp3!=None:#限公司|
                        if not re.search(r'经验|年|至|月|日期|第|时|周期|程师|项目一',projname_tmp3,re.I):
                            # print(projname_tmp3.group())
                            proj_exp['proj_name'].append(projname_tmp3.replace(' ', ''))
                            try:
                                line_tmp = re.sub(projname_tmp3,'',line_tmp)
                            except:
                                continue 
                    # print('name',flag)

                    
                    # 解析项目角色                          
                    projrole_tmp1 = re.search('[A-Za-z]*\s{0,1}[\u4e00-\u9fa5]*'.join(__job_list),line_tmp)
                    projrole_tmp2 = re.search(r'项\s*目\s*职\s*责|职\s*责|角\s色|责\s*任\s*描\s*述|职\s*能\s*描\s*述|负\s*责\s*模\s*块|负\s*责\s*内\s*容|主\s*要\s*负\s*责|职责描述', line_tmp)
                    
                    # jobname_tmp2 = re.search(r'java',line_tmp,re.I)
                    if projrole_tmp1:
                        flag1 = True
                        flag2 = False
                        if not re.search(r'与|和|配合|完成|及|根据|体验|的|为|等|负',projrole_tmp1.group()):                            
                            proj_exp['proj_role'].append(projrole_tmp1.group())
                    elif projrole_tmp2:
                        flag1 = True
                        flag2 = False
                    # print('role',flag)
                    
                    # 解析项目描述
                    projdisc_tmp = re.search(r'项\s*目\s*描\s*述|项\s*目\s*内\s*容|项\s*目\s*介\s*绍|简\s*介|项\s*目\s*概\s*述', line_tmp)
                    if projdisc_tmp:
                        flag1 = False
                        flag2 = True
                    if flag2 == True:
                        temp_list2 += line_tmp
                    if flag1 == True:
                        temp_list1 += line_tmp
                    # print('disc',flag)
                    
                    
            continue              
        else:
           continue    
    #work_exp['com_name'] = set(work_exp['com_name'])
    #work_exp['work_date'] = set(work_exp['work_date'])
    proj_exp['proj_role'] = [i for i in proj_exp['proj_role'] if i!='']
    proj_exp['proj_desc'] = [i for i in proj_exp['proj_desc'] if i!='']
    #work_exp['job_disc'][-len(work_exp['work_date']):]
    return proj_exp

def project_experience_extract(text):
    # data_list = []
    data = project_experience_extract_data(text)
    maxlength = max(len(data['proj_name']),len(data['proj_start_date']),len(data['proj_end_date']),len(data['proj_role']),len(data['proj_desc']))
    data['proj_name'].extend(' '*(maxlength-len(data['proj_name'])))
    data['proj_start_date'].extend(' '*(maxlength-len(data['proj_start_date'])))
    data['proj_end_date'].extend(' '*(maxlength-len(data['proj_end_date'])))
    data['proj_role'].extend(' '*(maxlength-len(data['proj_role'])))
    data['proj_desc'].extend(' '*(maxlength-len(data['proj_desc'])))
    data_tmp = sorted(list(zip(data['proj_name'],data['proj_start_date'],data['proj_end_date'],data['proj_role'],data['proj_desc'])),key=lambda x:x[1],reverse=True)
    return data_tmp
    # for i in range(len(data_tmp)):
    #     dic = {}
    #     dic['项目名称'] = data_tmp[i][0]
    #     dic['项目时间'] = data_tmp[i][1]
    #     dic['个人职责'] = data_tmp[i][2]
    #     dic['项目描述'] = data_tmp[i][3]
    #     data_list.append(dic)
    # if len(data_list)==0:
    #     return ''
    # else: return data_list


if __name__ == '__main__':
    """
    项目经历-项目名称
    项目经历-起止时间
    项目经历-项目角色
    项目经历-项目描述
    """
    
    file_paths, file_names = find_files(r'C:\Users\Wayne\Desktop\长亮科技\简历解析项目\gittest\长亮金服简历20220214')    
    df = pd.DataFrame(columns = ['filename','proj_name','proj_date','proj_role','proj_disc'])

    for path, name in zip(file_paths[:10], file_names[:10]):
        text = __extract_text(path)
        res = project_experience_extract(text)
        print(res,name)
    #     df = df.append({'filename': name,'proj_name':res['proj_name'],'proj_date':res['proj_date'],'proj_role':res['proj_role'],'proj_desc':res['proj_desc']},ignore_index = True)        
            
    # df.to_csv(r'project_experiences_results2.csv',encoding = 'utf-8-sig',index = False)