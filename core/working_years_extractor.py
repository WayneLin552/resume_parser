#!/root/anaconda3/bin/python

import re
import pdfplumber as pb
import os
import datetime

def working_date_extract(text):
    work_date = []
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)]
    for i in range(len(lines)):
        start_tag = re.search(r'就\s*职\s*公\s*司|作.{0,1}经.{0,1}历|作.{0,1}经.{0,1}验|工.{0,1}作.{0,1}经|.\s*作\s*背\s*景|工.*作.*履.*历|工.*作.*经.*历|公\s*司\s*经\s*历',lines[i])           
        if start_tag:
            for j in range(i, len(lines)):
                line_tmp = lines[j]            
                # 控制停止搜索标识
                end_tag = re.search(r'近\s*期\s*工\s*作|项\s*.\s*经\s*验|项\s*.\s*经\s*历|自\s*我\s*推\s*荐|自\s*我\s*评\s*价|项\s目\s经|专业技能|相关技能|证\s*书|在\s*校|意\s*向|电\s*话|手\s*机|求\s*职\s*意\s*向|邮\s*箱|性\s*别|籍\s*贯|学\s*历|年\s*龄|QQ|自\s*我\s*描\s*述|校\s*园\s*经\s*历|项\s*目\s*名|项\s*.\s*描\s*述|项\s*目\s*一|毕\s*业|项\s*.\s*背\s*景|职业培训|教育背景',line_tmp)
                if end_tag:
                    break
                else:
                    # 解析日期
                    date_tmp1 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月]*|.今|现在|\d{4}[\s年—－–\-~～/.\\]+.今)',line_tmp)
                    date_tmp2 = re.search(r'\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月—－–\-~～/.\\]+\d{1,2}[\s日]*[\s到至—－–\-~～/.\\]*(\d{4}[\s年—－–\-~～/.\\]+\d{1,2}[\s月—－–\-~～/.\\]+\d{1,2}[\s日]*|.今|现在)',line_tmp)                   
                    date_tmp3 = re.search(r'\d{4}[\s到至年—－–\-~～/.\\]+(\d{4}[\s年]*|.今|现在)',line_tmp)
                    if date_tmp1:
                        work_date.append(date_tmp1.group()) #|商务公司|银行
                    elif date_tmp2:
                        work_date.append(date_tmp2.group())   
                    elif date_tmp3:
                        work_date.append(date_tmp3.group())                     
        else:
           continue    
    return work_date


def working_years_extract(one_file_dir,text):
    '''
    工作时间查找，很多情况下文件名有，为了加快运行速度，先
    判断文件名有无给出信息，
    若没有进行关键词直接判断，
    若仍旧没有，用 工作经历 初略估计出一个值(不准确)
    输入：简历文件地址
    输出：str格式的工作年限，例如输入“/lmw简历.pdf”，输出'1'
    '''  
    #如果改接入函数的话(用self.__XXXX)要想办法获取文件名
    dic = {"一": 1,"二": 2,"三": 3,"四": 4,"五": 5,"六": 6,"七": 7,"八": 8,"九": 9}
    ans = re.search(r'[.\d\s]+年',one_file_dir,re.I)#先直接查找文件名，若找到返回，找不到进入文本内查找
    if ans:
        # print('method 1')
        return re.search(r'[.\d]+',ans.group()).group()
    else:
            #text = self.__extract_text() #模块中的extract_text    
            #实际上只需第一页内容就够了
        ans = re.search(r'.作年限[:：\s]*([一二三四五六七八九十]|\d{1,2}[.]{0,1}\d{0,2})|.作背景[:：\s]*([一二三四五六七八九十]|\d{1,2}[.]{0,1}\d{0,2})|.作时间[:：\s]*([一二三四五六七八九十]|\d{1,2}[.]{0,1}\d{0,2})|.作经验[:：\s]*([一二三四五六七八九十]|\d{1,2}[.]{0,1}\d{0,2}\s*年)|开发\s*[一二三四五六七八九十\d]+\s*年|.作经历[:：\s]*\d{1,2}[.]{0,1}\d{0,2}\s*年|[一二三四五六七八九十.\d\s]+年\s*.作经验|工作[\s.\d]年|[一二三四五六七八九十.\d\s]+年\s*.作经历|[一二三四五六七八九十.\d\s]+年\s*经验',text,re.I)
        #print(ans)
        if ans: #通过简历查找
            if re.search(r'[.\d]+|一|二|三|四|五|六|七|八|九|十',ans.group()):
                ans = re.search(r'[.\d]+|一|二|三|四|五|六|七|八|九|十',ans.group()).group() #应该没有奇葩写三位中文数字如 二十一 年吧...
                if re.search(r'\d{4}', ans):
                    # print('method 2')
                    return datetime.datetime.now().year-int(re.search(r'\d{4}', ans).group())
                else:
                    try:
                        return dic[re.search(r'[一二三四五六七八九十]',ans).group()]
                    except:
                        return ans
        else: #简历没直接写，通过 现在时间-毕业年份 间接查找
                # ans = re.search(r'\d{4}',__search_graduation_time(one_file_dir)[one_file_dir][0])
                # if ans:
                #     return datetime.datetime.now().year-int(ans.group())  #这一步很耗时，因为这个函数重复计算了毕业时间
                # #整合时可以考虑直接使用已经获得过的毕业时间，这样可以加快速度
                # else:
                #     return 'No Result'
            try:
                ans = re.search(r'\d{4}',sorted(working_date_extract(text))[0])
            except:
                return ''
            if ans:
                # print('method 3', ans.group())
                return datetime.datetime.now().year-int(ans.group())  #这一步很耗时，因为这个函数重复计算了毕业时间
            #整合时可以考虑直接使用已经获得过的毕业时间，这样可以加快速度
            else:
                return ''
    return ''



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


if __name__ == "__main__":
    file_paths, file_names = __find_files(r'C:\Users\Wayne\Desktop\长亮科技\简历解析项目\gittest\长亮金服简历20220214')
    working_years = {}
    for path, name in zip(file_paths,file_names):
        try:
            print(name)
            text=__extract_text(path)
            # print(working_years_extract(path),path)
            working_years[name] = working_years_extract(path,text)
        except:
            print(path)    
    
    
    import xlsxwriter as xw
    #写入excel方便算准确率
    
    def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
        workbook = xw.Workbook(fileName)  # 创建工作簿
        worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
        worksheet1.activate()  # 激活表
        title = ['文件名', '工作年限']  # 设置表头
        worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
        i = 2  # 从第二行开始写入数据
        for name, year in data.items():
            insertData = [name, year]
            row = 'A' + str(i)
            worksheet1.write_row(row, insertData)
            i += 1
        workbook.close()  # 关闭表
    
    xw_toExcel(working_years, 'working_years1.xlsx')

