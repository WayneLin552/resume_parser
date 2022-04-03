#!/root/anaconda3/bin/python

import os
import pdfplumber
import pandas as pd
import re


# set去重
__job_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/job_dic", 'r',encoding = 'utf-8')])
__job_list = list(__job_set)

# 去除空行
__job_list = [i for i in __job_list if i != '']

# set去重
__company_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/company_dic", 'r',encoding = 'utf-8')])
__company_list = list(__company_set)

# 去除空行
__company_list = [i for i in __company_list if i != '']


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
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:                
                text += page.extract_text() if page.extract_text() else ""
    except Exception as e:
        print(path,e)
    return text

def working_experience_extract_data(text):
    work_exp = {}
    work_exp['work_company'] = []
    work_exp['work_start_date'] = []
    work_exp['work_end_date'] = []
    work_exp['work_name'] = []
    work_exp['work_duty'] = []
    work_exp['work_desc'] = []  
    temp_list1 = ''
    temp_list2 = ''
    tempcompany_list = []
    # tempjob_list = []
    
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)] 
    # lines = re.split(r',|，|。|\t',text)
    for i in range(len(lines)):
        start_tag = re.search(r'就\s*职\s*公\s*司|作.{0,1}经.{0,1}验|作.{0,1}经.{0,1}历|工.{0,1}作.{0,1}经|.\s*作\s*背\s*景|工.*作.*履.*历|工.*作.*经.*历|公\s*司\s*经\s*历',lines[i])
            
        if start_tag is not None and len(lines[i])<=30:
            flag1 = False #直接插旗用排除法来一行行加入工作描述 
            flag2 = False #直接插旗用排除法来一行行加入工作职责
            flag3 = False #公司标识名额，以时间为识别符号
            flag4 = False #工作名字名额，以时间为识别符号
            mode = 0 #默认先公司后时间
            for j in range(i, len(lines)):
                line_tmp = lines[j]
                # 控制停止搜索标识 
                end_tag1 = re.search(r'项\s*.\s*经\s*验|项\s*.\s*经\s*历|意\s*向|自\s*我\s*推\s*荐|自\s*我\s*评\s*价|项\s目\s经|证\s*书|自\s*我\s*描\s*述|校\s*园\s*经\s*历|项\s*目\s*一|项\s*.\s*背\s*景|职\s*业\s*培\s*训|最\s*近\s*工\s*作|专\s*业\s*技\s*能|相\s*关\s*技\s*能|求\s*职\s*意\s*向|教\s*育\s*背\s*景|教\s*育\s*经\s*历|近\s*期\s*工\s*作|在\s*校|电\s*话[：:\s\d]+|手\s*机[：:\s\d]+|邮\s*箱[a-z：:\s\d]+|性\s*别[男女：:\s\d]+|籍\s*贯|学\s*历|年\s*龄[：:\s\d]+|QQ[：:\s\d]+|毕\s*业|校\s*内\s*经\s*历',line_tmp)
                # end_tag2 = re.search(r'项\s*.\s*经\s*验|项\s*.\s*经\s*历|意\s*向|自\s*我\s*推\s*荐|自\s*我\s*评\s*价|项\s目\s经|证\s*书|自\s*我\s*描\s*述|校\s*园\s*经\s*历|项\s*目\s*一|项\s*.\s*背\s*景|职\s*业\s*培\s*训',line_tmp)
                if end_tag1:
                    tempcompany_list = []
                    # work_exp['work_desc'].append(temp_list1)
                    # work_exp['work_duty'].append(temp_list2)
                    # temp_list1 = []
                    # temp_list2 = []
                    break
                # elif end_tag2:
                    # work_exp['work_desc'].append(temp_list1)
                    # work_exp['work_duty'].append(temp_list2)
                    # temp_list1 = []
                    # temp_list2 = []
                    # work_exp['work_desc'] = [i for i in work_exp['work_desc'] if i!=[]]
                    # work_exp['work_duty'] = [i for i in work_exp['work_duty'] if i!=[]]
                    # # if len(work_exp['work_name'])>len(work_exp['work_company']):
                    # #     num = len(work_exp['work_name'])-len(work_exp['work_company'])
                    # #     if num>len(tempcompany_list):
                    # #         work_exp['work_company'].append(tempcompany_list)
                    # #     else:
                    # #         work_exp['work_company'].append(tempcompany_list[-num:])
                    # work_exp['work_company'] = [i for i in work_exp['work_company'] if i!=[]]
                    # return work_exp               
                else:   
                    if len(work_exp['work_start_date'])>0 and len(tempcompany_list)==0:
                        #说明先时间后公司
                        mode = 1
                        #否则先公司后时间 mode=
                    
                    if re.search(r'该\s*公\s*司|[\u4e00-\u9fa5]{1,2}公司\s*[：:]',line_tmp):
                        line_tmp=re.sub('该\s*公\s*司|[\u4e00-\u9fa5]{1,2}公司\s*[：:]','', line_tmp)
                        
                     # 解析公司  医院|科技|股份公司|科技公司|集团|科技|商务公司|银行|责任公司|软件公司
                    company_tmp1 = re.search(r'[\u4e00-\u9fa5（）()0-9]+(公司|银行|科技|集团|医院|金融)',line_tmp)
                    company_tmp2 = re.search('|'.join(__company_list),line_tmp)
                    
                    if company_tmp1:
                        if not re.search(r'年度公司|与科技|分析金融科技|与集团|为集团|通过|保险科技|完善|同时|负责|期间|的|所属|上市|民营',company_tmp1.group()):
                            flag1 = False
                            flag2 = False
                            tempcompany_list.append(company_tmp1.group())
                            if flag3 == True and mode == 1: #先时间后公司
                                work_exp['work_company'].append(tempcompany_list[-1])
                                # tempcompany_list.pop()
                                flag3 = False
                                try:
                                    line_tmp = re.sub(company_tmp1.group(),'',line_tmp)
                                except:
                                    continue
                    elif company_tmp2:
                        
                        flag1 = False
                        flag2 = False
                        tempcompany_list.append(company_tmp2.group())
                        if flag3 == True and mode == 1: #先时间后公司
                            work_exp['work_company'].append(tempcompany_list[-1])
                            # tempcompany_list.pop()
                            flag3 = False
                        try:
                            line_tmp = re.sub(company_tmp2.group(),'',line_tmp)
                        except:
                            continue
                    
                    # 解析日期
                    date_tmp1 = re.search(r'20\d{2}[\s年—–－\-~～/.\\]+\d{1,2}[\s月]*[\s到至－—–\-~～/.\\]*(20\d{2}[\s年－—–\-~～/.\\]+\d{1,2}[\s月]*|.今|现在|20\d{2}[\s年—－–\-~～/.\\]+.今)',line_tmp)
                    date_tmp2 = re.search(r'20\d{2}[\s年—–－\-~～/.\\]+\d{1,2}[\s月－—–\-~～/.\\]+\d{1,2}[\s日]*[\s到至－—–\-~～/.\\]*(20\d{2}[\s年－—–\-~～/.\\]+\d{1,2}[\s月—－–\-~～/.\\]+\d{1,2}[\s日]*|.今|现在)',line_tmp)
                    date_tmp3 = re.search(r'20\d{2}[\s到至年—–－\-~～/.\\]+(20\d{2}[\s年]*|.今|现在)',line_tmp)   
                    
                    if date_tmp1:
                        flag1 = False
                        flag2 = False
                        flag3 = True
                        flag4 = True
                        if len(work_exp['work_start_date'])>0:
                            work_exp['work_desc'].append(temp_list1) 
                            temp_list1 = ''
                            work_exp['work_duty'].append(temp_list2) 
                            temp_list2 = ''
                        else:
                            temp_list1 = ''
                            temp_list2 = ''
                        
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp1.group()) if re.search(r'\d|今',i)]
                        if len(time)>3:
                            work_exp['work_start_date'].append('{}.{}'.format(time[0], time[1]))
                            work_exp['work_end_date'].append('{}.{}'.format(time[2], time[3]))
                        elif len(time)==3:                           
                            work_exp['work_start_date'].append('{}.{}'.format(time[0], time[1]))
                            work_exp['work_end_date'].append('{}'.format(time[2]))
                        # work_exp['work_date'].append(date_tmp1.group()) #|商务公司|银行
                        try:
                            if mode == 0 and flag3==True: #先公司后时间
                                work_exp['work_company'].append(tempcompany_list[-1])
                                # tempcompany_list.pop()
                                flag3 = False
                        except:
                            print('e')  
                        try:
                            line_tmp = re.sub(date_tmp1.group(),'',line_tmp)
                        except:
                            continue
                    elif date_tmp2:
                        flag1 = False
                        flag2 = False
                        flag3 = True
                        flag4 = True
                        if len(work_exp['work_start_date'])>0:
                            work_exp['work_desc'].append(temp_list1) 
                            temp_list1 = ''
                            work_exp['work_duty'].append(temp_list2) 
                            temp_list2 = ''
                        else:
                            temp_list1 = ''
                            temp_list2 = ''
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp2.group()) if re.search(r'\d|今',i)]
                        if len(time)>4:
                            work_exp['work_start_date'].append('{}.{}.{}'.format(time[0], time[1], time[2]))
                            work_exp['work_end_date'].append('{}.{}.{}'.format(time[3], time[4], time[5]))
                        elif len(time)==4:                           
                            work_exp['work_start_date'].append('{}.{}.{}'.format(time[0], time[1], time[2]))
                            work_exp['work_end_date'].append('{}'.format(time[3]))
                        # work_exp['work_date'].append(date_tmp2.group())
                        try:
                            if mode == 0 and flag3==True: #先公司后时间
                                work_exp['work_company'].append(tempcompany_list[-1])
                                # tempcompany_list.pop()
                                flag3 = False
                        except:
                            print('e')  
                        try:
                            line_tmp = re.sub(date_tmp2.group(),'',line_tmp)
                        except:
                            continue
                    elif date_tmp3:
                        flag1 = False
                        flag2 = False
                        flag3 = True
                        flag4 = True
                        if len(work_exp['work_start_date'])>0:
                            work_exp['work_desc'].append(temp_list1) 
                            temp_list1 = ''
                            work_exp['work_duty'].append(temp_list2) 
                            temp_list2 = ''
                        else:
                            temp_list1 = ''
                            temp_list2 = ''
                        time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',date_tmp3.group()) if re.search(r'\d|今',i)]
                        if len(time)==2:
                            work_exp['work_start_date'].append('{}'.format(time[0]))
                            work_exp['work_end_date'].append('{}'.format(time[1]))
                        # work_exp['work_date'].append(date_tmp3.group())
                        try:
                            if mode == 0 and flag3==True: #先公司后时间
                                work_exp['work_company'].append(tempcompany_list[-1])
                                # tempcompany_list.pop()
                                flag3 = False
                        except:
                            print('e')  
                        try:
                            line_tmp = re.sub(date_tmp3.group(),'',line_tmp)
                        except:
                            continue
                    # print('date:',flag1,flag2)                   
                    # print(mode)
                    # print(tempcompany_list)
                    
                    # 解析工作名称                          
                    jobname_tmp1 = re.search('|[A-Za-z]*\s{0,1}[\u4e00-\u9fa5]*'.join(__job_list),line_tmp)
                    # jobname_tmp2 = re.search(r'java',line_tmp,re.I)
                    if jobname_tmp1:
                        if not re.search(r'有|在|收集|带出|协助|对|从|了|与|和|配合|完成|及|根据|体验|的|为|等|负|担任|应用|国际化|住|车主|外派|找|将|于|是|获得|主要|保险科技',jobname_tmp1.group()):   
                            flag1 = False
                            flag2 = False
                            # tempjob_list.append(jobname_tmp1.group())
                            if flag4 == True:
                                work_exp['work_name'].append(jobname_tmp1.group())
                                flag4 = False
                    # print('job:',flag1,flag2)

                    
                    # 解析工作职责
                    jobduty_tmp = re.search(r'个\s*人\s*职\s*责|工\s*作\s*职\s*责|主\s*要\s*职\s*责|责\s*任\s*描\s*述|工\s*作\s*职\s*责|岗\s*位\s*职\s*责|职\s*责[：:\s]+|描\s*述[:：\s]+|主\s*要\s*负\s*责',line_tmp)
                    if jobduty_tmp:
                        # print(jobduty_tmp.group())
                        flag1 = False
                        flag2 = True                                             
                    # print('duty:',flag1,flag2)
                    # 解析工作描述
                    jobdesc_tmp = re.search(r'工\s*作\s*描\s*述|工\s*作\s*内\s*容|职\s*责\s*业|内\s*容[:：\s]+|负\s*责.*工\s*作|介\s*绍[\s：:]+', line_tmp)
                    if jobdesc_tmp:
                        # print(jobdesc_tmp.group())
                        flag1 = True
                        flag2 = False
                    # print('desc:',flag1,flag2)
                    if flag1 == True and flag2 == False:
                        # temp_list1.append(line_tmp)
                        temp_list1 += line_tmp
                    if flag2 == True:
                        # temp_list2.append(line_tmp)
                        temp_list2 += line_tmp
                    flag1 = True    
                continue        
        else:
           continue   
    work_exp['work_desc'].append(temp_list1)
    work_exp['work_duty'].append(temp_list2)
    temp_list1 = ''
    temp_list2 = ''
    work_exp['work_desc'] = [i for i in work_exp['work_desc'] if i!='']
    work_exp['work_duty'] = [i for i in work_exp['work_duty'] if i!='']
    # if len(work_exp['work_name'])>len(work_exp['work_company']):
    #     num = len(work_exp['work_name'])-len(work_exp['work_company'])
    #     if num>len(tempcompany_list):
    #         work_exp['work_company'].append(tempcompany_list)
    #     else:
    #         work_exp['work_company'].append(tempcompany_list[-num:])
    work_exp['work_company'] = [i for i in work_exp['work_company'] if i!=[]]
    return work_exp

def working_experience_extract(text):
    # data_list = []
    data = working_experience_extract_data(text)
    maxlength = max(len(data['work_company']),len(data['work_start_date']),len(data['work_end_date']),len(data['work_name']),len(data['work_duty']),len(data['work_desc']))
    data['work_company'].extend(' '*(maxlength-len(data['work_company'])))
    data['work_start_date'].extend(' '*(maxlength-len(data['work_start_date'])))
    data['work_end_date'].extend(' '*(maxlength-len(data['work_end_date'])))
    data['work_name'].extend(' '*(maxlength-len(data['work_name'])))
    data['work_duty'].extend(' '*(maxlength-len(data['work_duty'])))
    data['work_desc'].extend(' '*(maxlength-len(data['work_desc'])))
    data_tmp = sorted(list(zip(data['work_company'],data['work_start_date'],data['work_end_date'],data['work_name'],data['work_duty'],data['work_desc'])),key=lambda x:x[1],reverse=True)
    return data_tmp
    # for i in range(len(data_tmp)):
    #     dic = {}
    #     dic['公司名称'] = data_tmp[i][0]
    #     dic['起止时间'] = data_tmp[i][1]
    #     dic['职位'] = data_tmp[i][2]
    #     dic['工作职责'] = data_tmp[i][3]
    #     dic['工作描述'] = data_tmp[i][4]
    #     data_list.append(dic)
    # if len(data_list)==0:
    #     return ''
    # else: return data_list



# if __name__ == '__main__':
    
#     file_paths, file_names = find_files(r'C:\Users\Wayne\Desktop\长亮科技\简历解析项目\gittest\长亮金服简历20220214')    
#     df = pd.DataFrame(columns = ['filename','com_name','work_date','job_name','job_res','job_disc'])

#     for path, name in zip(file_paths[:10], file_names[:10]):
#         text = __extract_text(path)
#         res = working_experience_extract(text)
#         print(res,name)
    #     df = df.append({'filename': name,'com_name':res['work_company'],'work_date':res['work_date'],\
    #                 'job_name':res['work_name'],'job_res':res['work_duty'],'job_disc':res['work_desc']},ignore_index = True)        
            
    # df.to_csv(r'working_experiences_results1_3.csv',encoding = 'utf-8-sig',index = False)