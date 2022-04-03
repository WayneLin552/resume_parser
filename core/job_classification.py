# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:04:02 2022

@author: LinMouwei
"""

import pandas as pd
# import pkuseg
import os
# from collections import Counter 
import re
# def job_classification(path):
#     csv = pd.read_csv(path,encoding='utf-8')

path3=os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
path2 = path3 + r'\docs_dics\招聘关键字_csv.csv'
path = r'C:\Users\Wayne\Desktop\招聘关键字.xlsx' 
df = pd.read_csv(path2,encoding='utf-8-sig') 
               
def job_classification(text):
    dic = {}   
    posi = []
    key = []
    for position,keywords in zip(df['岗位'],df['招聘关键字']):
        dic[position] = [0]       
        for keyword in list(i for i in re.split(r'\', \'|\[\'|\'\]',keywords) if i != ''):          
            if str.lower(keyword) in str.lower(text):
                dic[position][0] += 1
                dic[position].append(keyword)
    tmp = sorted(dic.items(),key=lambda x:x[1][0],reverse=True)[:4]
    for i in range(len(tmp)):
        posi.append(tmp[i][0])
        key.append(tmp[i][1][1:])
    return posi,sorted(list(set(sum(key,[]))))


if __name__=='__main__':
    # result = []
    # textall = pd.read_csv(path3+r'\result\base_info_result.csv',encoding='utf-8-sig')
    # for i in range(len(textall['skills'][1:])):
    #     if str(textall['skills'][i+1]) != 'nan':
    #         res = job_classification(textall['skills'][i+1])
    #         result.append([textall['filename'][i+1],res])            
    #     else:
    #         result.append([textall['filename'][i+1],'None'])
    
    
    
    # df = pd.read_excel(path)
    dic = {}
    # text ='专业技能熟练使用Axure、墨刀、Visio、Xmind、禅道等软件，快速绘制产品原型、脑图，输出产品需求文档及业务流程图。熟悉数据分析的方法和过程，能够运用相关数据分析方法对产品进行相关分析。熟悉APP/SDK、小程序、桌面客户端开发设计的流程。有后端开发经验，熟悉后端开发技术及相关流程。ToC、ToB产品经验，熟练掌握用户研究、用户体验、需求挖掘、产品规划等相关技能。'
    # res = job_classification(text)
    da = pd.DataFrame(columns=['岗位','招聘关键字'])
    for position, keywords in zip(df['岗位'],df['招聘关键字']):
        for keyword in list(set(str.lower(i) for i in re.split(r'\', \'|\[\'|\'\]',keywords) if i != '')):
            if str.lower(position) in dic:
                try:
                    int(keyword)
                except:
                    dic[str.lower(position)].append(keyword)
            else:
                dic[str.lower(position)] = []
                try:
                    int(keyword)
                except:
                    dic[str.lower(position)].append(keyword)        
    for key,item in dic.items():
        item=list(set(item))      
        da=da.append({'岗位':key,'招聘关键字':item},ignore_index=True)
    da.to_csv(path2,encoding='utf-8-sig')
    # pass
    

    
    
    # seg = pkuseg.pkuseg(postag=True)
    # text=re.split(r'熟练掌握|掌握|熟悉|了解|熟练','编程语言：  熟练使用 Java 语言 , 熟悉 Python、Scala 语言开发工具：  熟练使用 Eclipse、IDEA、PyCharm，项目管理工具 Maven开发组件 :1，熟悉 Linux 开发环境,熟、Hadoop 集群搭建2，熟悉使用 SQL 语言,熟悉 MySQL 数据库3，熟悉 HDFS、MapReduce、YARN、Hive、HBase、Zookeeper、Kafka 等 Hadoop 生态圈相关组件4，熟练使用 MapReduce、Spark 计算框架编程5，熟练运用 Hive 数据仓库工具，对数据进行查询，统计等数据操作;6，熟悉HBase 数据库的使用，理解HBase 的存储原理和存储架构7，熟练使用 oozie 和 linux 的任务调度机制8，熟悉 Spark Streaming 对接实现流式数据的过滤和分析')
    # # rst = seg.cut('"		熟练掌握：软件测试技术，软件测试流程，软件测试方法等；		熟练掌握：设计与执行测试用例，发现并跟踪bug；		掌握：接口测试，性能测试。能够使用postman等工具。熟悉fiddler抓包工具。		掌握:   会搭建LAMP测试环境；		掌握：使用过Git版本控制软件；		掌握：MySQL 数据库，掌握 SQL 语言；		掌握：Linux常用命令；		掌握：计算机网络基础，HTTP/HTTPS，TCP/IP网络协议;		了解：h5，js，css前端开发语言。		"')
    # # rst = list(set(rst))
    # for i in text:
    #     rst = seg.cut(i)
    #     rst = [i for i in rst ]#if i[1] == 'n' or i[1]=='vn' or i[1]=='i']
    #     print(rst)
    # Counter(rst)
    # print(rst)
    
    # Excel熟练使用透视表、切片器；表单控件； 、 。PowerPivot PowerQueryMySQL
    # 熟练数据库语言、能在 环境下对数据进行增删改查。HiveSQLPython熟悉 基本语法，
    # 、 进行数据清洗、数据探索以及python Numpy Pandas等进行数据可视化展示。
    # Matplotlib, Seaborn了解 、 、逻辑回归、决策树、随机森林等算法原理。
    # KNN K-meansTableau熟练运用参数设计，度量计算等实现多维度监控报表及可视化呈现。
    # Power BI掌握多种数据源的加载、多表的 图联接、 的数据修改、ER power query的数据建模和展示。
    # power pivot其他可视化， 绘图， 动画设计， 三维动画等。MATLAB AutoCAD Flash Maya