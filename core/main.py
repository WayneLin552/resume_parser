#!/root/anaconda3/bin/python
import re
import os
import pdfplumber as pb
import pandas as pd
#from win32com.client import Dispatch
import sys
#import docx2txt
import subprocess
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from logconf.log_settings import Logger

# import configparser
from core.name_extractor import name_extract
import core.docx2txt as docx2txt
from core.gender_extractor import gender_extract
from core.age_extractor import age_extract
from core.degree_extractor import degree_extract
from core.school_extractor import school_extract
from core.graduation_time_extractor import graduation_time_extract
from core.working_years_extractor import working_years_extract
from core.major_extractor import major_extract
from core.position_extractor import position_extract
from core.phone_extractor import phone_extract
from core.email_extractor import email_extract
from core.education_experience_extractor import education_experience_extract
from core.working_experience_extractor import working_experience_extract
from core.project_experience_extractor import project_experience_extract
from core.skills_extractor import skills_extract
from core.job_classification import job_classification



# #读取配置文件
# config = configparser.ConfigParser()
# config.read(r'logconf\config.ini')


# log_dir = config['DEFAULT']['log_dir']
# output_dir = config['DEFAULT']['output_dir']


# # 创建日志目录
# if not os.path.exists(log_dir):
#     os.mkdir(log_dir)
#  # 创建结果文件目录
# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)





def __find_files(file_dir):
    """迭代查找文件"""
    file_paths = []
    file_names = []
    tmp_file_names = []
    hr_names = []
    # set去重
    __file_set = set([i.strip() for i in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/file_dic", 'r',encoding = 'utf-8')])
    __file_list = list(__file_set)
    # 去除空行
    __file_list = [i for i in __file_list if i != '']
    file_list = __file_list
    f = open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/file_dic", 'w',encoding = 'utf-8')
    for root, _, files in os.walk(file_dir):
        for file in files:
            path = os.path.join(root,file)
            rear = os.path.splitext(path)[1]
            if rear in [".doc", ".docx", ".pdf"]: #本处只考虑pdf
                tmp_file_names.append(file)
                if file not in file_list:
                    f.write(file+'\n')
                    file_paths.append(path)
                    file_names.append(file)
                    hr_names.append(os.path.split(os.path.dirname(path))[1]) 
    for i in range(len(file_list)):
        if file_list[i] not in tmp_file_names:
            file_list[i] = ''
    file_list = [i for i in file_list if i != '']  
    for i in range(len(file_list)):
        f.write(file_list[i]+'\n')       
    f.close()        
    return file_paths, file_names, hr_names

# for windows system 
def __doc2docx2(path):
    # print('1',path)
        # if system == 'win':
    from win32com.client import Dispatch
    word = Dispatch('Word.Application')
    try:
        doc = word.Documents.Open(path)
        new_path = os.path.splitext(path)[0] + '.docx'
        doc.SaveAs(new_path, FileFormat=12) # wdFormatPDF
        doc.Close()
    except Exception as e:
        print(path,e)
    word.Quit()

#专门针对.doc文件打开乱码问题
def mime_version(text):
    get = re.findall(r' >[^a-zA-Z]+<|<br>', text)
    text_end = ''
    for i in get:
        if i!='<br>' :
            temp = re.sub('>|<', '', i)
            temp = re.sub('。|;|；|\|', '\n', temp)
            text_end += temp
        else:
            text_end += '\n'
    return text_end


# for linux system    
def __doc2docx(path):   
    try:
        subprocess.run(["soffice","--headless","--invisible","--convert-to","docx",path,"--outdir",os.path.split(path)[0]+'/'])
    except Exception as e:
        print(path,e)


def __extract_text(path):
    """
    抽取文本内容
    """
    text = ''
    try:
        if os.path.splitext(path)[1] == ".pdf":
            pdf = pb.open(path)
            for page in pdf.pages:               
                text += page.extract_text() if page.extract_text() else ""
        elif os.path.splitext(path)[1] == ".doc":
            __doc2docx(path)
            text = docx2txt.process(os.path.splitext(path)[0] + '.docx')
            os.remove(os.path.splitext(path)[0] + '.docx')
            return text
        elif os.path.splitext(path)[1] == '.docx':
            text = docx2txt.process(path)
            return text
    except:# Exception as e:
        print(path)
    return text

def __extract_text2(path):
    """
    抽取文本内容
    """
    text = ''
    try:
        if os.path.splitext(path)[1] == ".pdf":
            pdf = pb.open(path)
            for page in pdf.pages:               
                text += page.extract_text() if page.extract_text() else ""
        elif os.path.splitext(path)[1] == ".doc":
            __doc2docx2(path)
            text = docx2txt.process(os.path.splitext(path)[0] + '.docx')
            os.remove(os.path.splitext(path)[0] + '.docx')
            return text
        elif os.path.splitext(path)[1] == '.docx':
            text = docx2txt.process(path)
            return text
    except:# Exception as e:
        print(path)
    return text

    
def total_extract(path,system='linux'):
    # 创建日志文件
    dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file_dir = dirname + '/log/resume_extractor.log'
    log = Logger(log_file_dir,level = 'info')        
    log.logger.info('Program Start...')    
    log.logger.info('Try to update resumes date, at '+ time.ctime(time.time()))
    time.localtime()
    files,names,hr_names = __find_files(path)
    update_time = time.ctime(time.time())
    df_base = pd.DataFrame(columns = ['filename','hr_name','name','gender','age','phone','email','degree','school',\
                                  'major','grad_time','working_years','position','skills','update_time'])
                                      
    df_edu = pd.DataFrame(columns=['filename','hr_name','edu_school','edu_start_date','edu_end_date','edu_major','edu_degree','update_time'])
    df_work = pd.DataFrame(columns=['filename','hr_name','work_company','work_start_date','work_end_date','work_name','work_duty','update_time'])
    df_proj = pd.DataFrame(columns=['filename','hr_name','proj_name','proj_start_date','proj_end_date','proj_role','proj_desc','update_time'])
    df_keyw = pd.DataFrame(columns=['filename','position_recog','keywords'])
    
    # 提取简历信息  
    log.logger.info('extract resume info...')
    len_names = len(names)
    log.logger.info('Update Files: '+str(len_names))
    # print('Update Files:',len(names))
    try:
        for i,name,hr in zip(files,names,hr_names):
            if system == 'linux':
                text = __extract_text(i)
            elif system == 'win':
                text = __extract_text2(i)
            if 'MIME-version: 1.0' in text:
                text = mime_version(text)
            posi,key = job_classification(text)
            basename = os.path.basename(i)
            res_name = name_extract(text,i)
            res_gender = gender_extract(text)
            res_age = age_extract(text)
            res_phone = phone_extract(text)
            res_email = email_extract(text)
            res_degree = degree_extract(text)
            res_school = school_extract(text)
            res_grad_time = graduation_time_extract(text)
            res_major = major_extract(text)
            res_working_years = working_years_extract(i,text)
            res_position = position_extract(basename)
            res_edu_exp = education_experience_extract(text)
            res_work_exp = working_experience_extract(text)
            res_proj_exp = project_experience_extract(text)
            res_skill = skills_extract(text)   
            df_keyw = df_keyw.append({'filename':name,'position_recog':posi,'keywords':key},ignore_index=True)
            df_base = df_base.append({'filename':name,'hr_name':hr,'name':res_name,'gender':res_gender,'age':res_age,'phone':res_phone,'email':res_email,'degree':res_degree,'school':res_school,\
                                  'major':res_major,'grad_time':res_grad_time,'working_years':res_working_years,'position':res_position,'skills':res_skill,'update_time':update_time},ignore_index = True)            
            for i in range(len(res_edu_exp)):
                df_edu = df_edu.append({'filename':name,'hr_name':hr,'edu_school':res_edu_exp[i][0],'edu_start_date':res_edu_exp[i][1],'edu_end_date':res_edu_exp[i][2],'edu_major':res_edu_exp[i][3],'edu_degree':res_edu_exp[i][4],'update_time':update_time,'update_time':update_time},ignore_index = True)    
            for i in range(len(res_work_exp)):
                df_work = df_work.append({'filename':name,'hr_name':hr,'work_company':res_work_exp[i][0],'work_start_date':res_work_exp[i][1],'work_end_date':res_work_exp[i][2],'work_name':res_work_exp[i][3],'work_duty':res_work_exp[i][4],'work_desc':res_work_exp[i][5],'update_time':update_time},ignore_index = True)          
            for i in range(len(res_proj_exp)):
                df_proj = df_proj.append({'filename':name,'hr_name':hr,'proj_name':res_proj_exp[i][0],'proj_start_date':res_proj_exp[i][1],'proj_end_date':res_proj_exp[i][2],'proj_role':res_proj_exp[i][3],'proj_desc':res_proj_exp[i][4],'update_time':update_time},ignore_index = True)
    except Exception as e:
        print('行号', e.__traceback__.tb_lineno, name)
        log.logger.error(e)
        sys.exit(1)     
    # 保存解析结果  
    
    try: 
        temp_path = os.sys.path[-1]
        if os.path.exists(temp_path+r'/result/base_info_result.csv'):          
            df_base.to_csv(temp_path+r'/result/base_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        else: df_base.to_csv(temp_path+r'/result/base_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        if os.path.exists(temp_path+r'/result/edu_exp_info_result.csv'):
            df_edu.to_csv(temp_path+r'/result/edu_exp_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        else: df_edu.to_csv(temp_path+r'/result/edu_exp_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        if os.path.exists(temp_path+r'/result/work_exp_info_result.csv'):
            df_work.to_csv(temp_path+r'/result/work_exp_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        else: df_work.to_csv(temp_path+r'/result/work_exp_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        if os.path.exists(temp_path+r'/result/proj_exp_info_result.csv'):
            df_proj.to_csv(temp_path+r'/result/proj_exp_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        else: df_proj.to_csv(temp_path+r'/result/proj_exp_info_result.csv',encoding = 'utf-8-sig',index = False,mode='w')
        if os.path.exists(temp_path+r'/result/keyw_info_result.csv'):
            df_keyw.to_csv(temp_path+r'\result\keyw_info_result.csv',encoding='utf-8-sig',index=False,mode='a')
        else:
            df_keyw.to_csv(temp_path+r'\result\keyw_info_result.csv',encoding='utf-8-sig',index=False,mode='w')
        log.logger.info('save result file...')
    except Exception as e:
        print('error',name)
        log.logger.error(e)
        sys.exit(1)          
 
    log.logger.info('Program end successfully at '+time.ctime(time.time()))
    
if __name__ == '__main__':
    path = r'C:\Users\Wayne\Desktop\changlian\resume_ana\gittest\resume_parser\docs_dics\resumes'
    # df = pd.DataFrame(columns=['filename','position_rec','keywords'])
    df = pd.DataFrame(columns=['filename','name'])
    files,names,hrs = __find_files(path)
    for i,name,hr in zip(files,names,hrs):
        text = __extract_text2(i)
        # posi,key = job_classification(text)
        # df = df.append({'filename':name,'position_rec':posi,'keywords':key},ignore_index=True)
        minzi = name_extract(text,i)
        df = df.append({'filename':name,'name':minzi},ignore_index=True)
    # df.to_csv(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+r'\result\posi_keywords.csv',encoding='utf-8-sig',index=False)
    df.to_csv(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+r'\result\name.csv',encoding='utf-8-sig',index=False)   
    
    # pass
    
    # path = r'../docs_dics/resumes'   
    # path = os.path.abspath(path)
    # time1 = time.time()
    # total_extract(path,'linux')
    # time2 = time.time()-time1
    # print('total time:',time2)
    
