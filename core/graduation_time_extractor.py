#!/root/anaconda3/bin/python
# coding: utf-8

import re
import pdfplumber as pb
import os
#林谋伟_实习生
#简历解析-毕业时间识别
#20220223
#v1.0.3

#def __search_graduation_time(self): 换成这个
def graduation_time_extract_data(text):
    '''  输入：文件地址
    输出：一个str格式的日期
    例如：输入/lmw简历.pdf    输出：'2022/06'   
    后面整合的时候改为self.__XXXX时候要做一些更改，主要是获取test内容那几行
    '''
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)]
    for i in range(len(lines)):  #一行行找，看是否有教育相关关键词 毕\s*业\s*学\s*校|毕\s*业\s*院\s*校|专\s*业|学\s*历
        if re.findall(r'教\s*育\s*背\s*景|教\s*育\s*经\s*历|毕\s*业\s*时\s*间|学\s*习\s*经\s*历|毕\s*业\s*年\s*限|就\s*读\s*时\s*间',lines[i],re.I):
            ans1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|\d{4}[\s年—－–\-~～/.\\]+.今)',lines[i],re.I)
            ans2 = re.search(r'\d{4}[\s年到至—－–\-~～/.\\]+(\d{4}[\s年]*|.今)',lines[i],re.I)
            ans3 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|\d{4}[\s年]*',lines[i],re.I)
            if ans1: #若关键词所在那一行有日期
                return re.findall(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今',ans1.group())[-1]
            elif ans2:
                return re.findall(r'\d{4}[\s年]*|.今',ans2.group())[-1]
            elif ans3:
                return ans3.group()
            elif (i+1)<len(lines): #否则查找下一行
                ans1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|\d{4}[\s年—－–\-~～/.\\]+.今)',lines[i+1],re.I)
                ans2 = re.search(r'\d{4}[\s年到至—－–\-~～/.\\]+(\d{4}[\s年]*|.今)',lines[i+1],re.I)
                ans3 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|\d{4}[\s年]*',lines[i+1],re.I)
                if ans1: #若关键词所在那一行有日期
                    return re.findall(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今',ans1.group())[-1]
                elif ans2:
                    return re.findall(r'\d{4}[\s年]*|.今',ans2.group())[-1]
                elif ans3:
                    return ans3.group()
                elif (i+2)<len(lines):
                    ans1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|\d{4}[\s年—－–\-~～/.\\]+.今)',lines[i+2],re.I)
                    ans2 = re.search(r'\d{4}[\s年到至—－–\-~～/.\\]+(\d{4}[\s年]*|.今)',lines[i+2],re.I)
                    ans3 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|\d{4}[\s年]*',lines[i+2],re.I)
                    if ans1: #若关键词所在那一行有日期
                        return re.findall(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今',ans1.group())[-1]
                    elif ans2:
                        return re.findall(r'\d{4}[\s年]*|.今',ans2.group())[-1]
                    elif ans3:
                        return ans3.group()
                    elif (i+3)<len(lines):
                        ans1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|\d{4}[\s年—－–\-~～/.\\]+.今)',lines[i+3],re.I)
                        ans2 = re.search(r'\d{4}[\s年到至—－–\-~～/.\\]+(\d{4}[\s年]*|.今)',lines[i+3],re.I)
                        ans3 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|\d{4}[\s年]*',lines[i+3],re.I)
                        if ans1: #若关键词所在那一行有日期
                            return re.findall(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今',ans1.group())[-1]
                        elif ans2:
                            return re.findall(r'\d{4}[\s年]*|.今',ans2.group())[-1] 
                        elif ans3:
                            return ans3.group()
                        elif (i+4)<len(lines):
                            ans1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|\d{4}[\s年—－–\-~～/.\\]+.今)',lines[i+4],re.I)
                            ans2 = re.search(r'\d{4}[\s年到至—－–\-~～/.\\]+(\d{4}[\s年]*|.今)',lines[i+4],re.I)
                            ans3 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|\d{4}[\s年]*',lines[i+4],re.I)
                            if ans1: #若关键词所在那一行有日期
                                return re.findall(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今',ans1.group())[-1]
                            elif ans2:
                                return re.findall(r'\d{4}[\s年]*|.今',ans2.group())[-1]
                            elif ans3:
                                return ans3.group()
        else:
            continue 
        
    for line in lines:
        if re.search(r'专\s*业|毕业院校|学\s*历|[\u4e00-\u9fa5]+(大学|学院|学校|高中|初中|理工)',line):
            ans1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|\d{4}[\s年—－–\-~～/.\\]+.今)',line,re.I)
            ans2 = re.search(r'\d{4}[\s年到至—－–\-~～/.\\]+(\d{4}[\s年]*|.今)',line,re.I)
            ans3 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|\d{4}[\s年]*',line,re.I)
            if ans1: #若关键词所在那一行有日期
                return re.findall(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今',ans1.group())[-1]
            elif ans2:
                return re.findall(r'\d{4}[\s年]*|.今',ans2.group())[-1]
            elif ans3:
                return ans3.group()
        else: 
            continue
    return ''

def graduation_time_extract(text):
    data = graduation_time_extract_data(text)
    time = [re.search(r'\d+|.*今',i).group() for i in re.split(r'[^\d至今\t]',data) if re.search(r'\d|今',i)]
    if len(time)==2:
        return '{}.{}'.format(time[0], time[1])
    elif len(time)==1:                           
        return '{}'.format(time[0])
    elif len(time)==3:
        return '{}.{}.{}'.format(time[0], time[1], time[2])
    else: return ''
    


def __find_files(file_dir):
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
            pdf = pb.open(path)
            for page in pdf.pages:
                
                text += page.extract_text() if page.extract_text() else ""
    except Exception as e:
        print(path,e)
    return text


# if __name__ == "__main__":
    
#     graduation_time = {}
#     file_paths, file_names = __find_files(r'C:\Users\Wayne\Desktop\gittest\长亮金服简历20220214')
#     for path, name in zip(file_paths, file_names):
#         try:
#             text = __extract_text(path)
#             print(name)
#             graduation_time[name] = graduation_time_extract(text)
#         except:
#             print(path)
    
#     import xlsxwriter as xw
#     #输出到excel表中方便计算准确率
    
#     def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
#         workbook = xw.Workbook(fileName)  # 创建工作簿
#         worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
#         worksheet1.activate()  # 激活表
#         title = ['文件名', '毕业时间']  # 设置表头
#         worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
#         i = 2  # 从第二行开始写入数据
#         for name, year in data.items():
#             insertData = [name, year]
#             row = 'A' + str(i)
#             worksheet1.write_row(row, insertData)
#             i += 1
#         workbook.close()  # 关闭表
     
     
#     xw_toExcel(graduation_time, 'graduation_time1_1.xlsx')



