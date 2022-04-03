    #!/root/anaconda3/bin/python
import os
import re 
import pdfplumber
import pandas as pd
# from win32com.client import Dispatch

# set去重
__major_set = set([v.strip() for v in open(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+"/docs_dics/major_dic", 'r',encoding = 'utf-8')])

__major_list = list(__major_set)

# 去除空行
__major_list = [i for i in __major_list if i != '']

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

def major_extract(text):
    major = []
    tempmajor_list = []
    tempschool_list = []
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)] 
    
    # for line in lines:
    #     major_tmp = re.search('|'.join(__major_list),line)
    #     if major_tmp:
    #         major.append(major_tmp.group())
    #         break
    
    # # 去重
    # major = list(set(major))
    for i in range(len(lines)):
        #先从关键字查找
        start_tag = re.search(r'教.{0,1}育.{0,1}背.{0,1}景|教.{0,1}育.{0,1}经.{0,1}历',lines[i])            
        if start_tag:
            flag = False #major名额，以学校为识别符号
            mode = 0 #默认先学校后专业
            # print(lines[i],start_tag.group())
            for j in range(i, len(lines)):
                line_tmp = lines[j]               
                # 控制停止搜索标识
                end_tag = re.search(r'工\s*作|项\s*目|技\s*能|评\s*价|证\s*书|能\s*力|在\s*校|培\s*训|实\s*习',line_tmp)
                if end_tag:
                    if len(major)==0:
                        break
                    else:
                        major = list(set(major))
                        temp = ''
                        for i in major:
                            temp += i+'、'
                        return temp[:-1]
                else:    
                    if len(tempschool_list)==0 and len(tempmajor_list)>0:
                        #说明先专业后学校
                        mode = 1
                        #否则先学校后专业 mode=1
                    school_tmp = re.search("([\s]*)([\u4e00-\u9fa5]{2,15}(大学|学院|中学|学校|高中|初中))", line_tmp)
                    if school_tmp:
                        flag = True
                        tempschool_list.append(school_tmp.group())
                        if flag == True and mode == 1: #先专业后学校
                            major.append(tempmajor_list[-1])
                            tempmajor_list.pop()
                            flag = False
                        try:
                            line_tmp = re.sub(school_tmp.group(),'',line_tmp)
                        except:
                            continue
                        
                    major_tmp = re.search('|'.join(__major_list),line_tmp)
                    if major_tmp:
                        # print('method 1')
                        # major_tmp = re.sub(r'[^\u4e00-\u9fa5]*','',major_tmp.group())
                        tempmajor_list.append(major_tmp.group())
                        if flag == True and mode == 0: #先学校后专业
                            major.append(tempmajor_list[-1])
                            tempmajor_list.pop()
                            flag = False
                        try:
                            line_tmp = re.sub(major_tmp.group(),'',line_tmp)
                        except:
                            continue
                    # print('made:',mode)
                 
            break
            # return major              
        else:
           continue 
    # re.sub(pattern, repl, string)
    #若找不到，从文本直接找
    if len(major)==0:
        for line in lines:
            major_tmp = re.search('|'.join(__major_list),line)
            if major_tmp:
                major.append(major_tmp.group())
                # print('method 2')
                break
    # major=list(set(major))  
    if len(major)==0:
        return ''
    else: 
        major = list(set(major))
        temp = ''
        for i in major:
            temp += i+'、'
            return temp[:-1]


if __name__ == '__main__':        
    
    path = r'C:\Users\Wayne\Desktop\长亮科技\简历解析项目\gittest\长亮金服简历20220214'
    files,names = find_files(path)
    
    # for i in files:
    #     if os.path.splitext(i)[1] in ['.doc','.docx']:
    #         __doc2pdf(os.path.abspath(i))
    
    # files = [os.path.splitext(i)[0] + '.pdf' if os.path.splitext(i)[1] in ['.doc','.docx'] else i for i in files]
    # files = [os.path.abspath(i) for i in files]
    # files = list(set(files))

    df = pd.DataFrame(columns = ['filename','major'])

    for i,name in zip(files,names):
        text = __extract_text(i)
        res = major_extract(text)
        print(name)
        df = df.append({'filename': name,'major':res},ignore_index = True)

            
    df.to_csv(r'major_results1.csv',encoding = 'utf-8-sig',index = False)
    