#!/root/anaconda3/bin/python

import re


def degree_extract(text):
    '''
    获取学历

    Parameters
    ----------
    text: string
        简历解析后的文本

    Returns: string
    -------
        学历 / ''
    '''
    
    dic = {'博士':0,'本科':0,'学士':0,'专科':0,'大专':0,'中专':0,'职高':0,'高中':0,'初中':0}
    #按照学位高低由高到低存到字典
    education = re.findall(r"博\s*士|硕\s*士|本\s*科|学\s*士|专\s*科|大\s*专|中\s*专|职\s*高|高\s*中|初\s*中", text)
    if education:
        for edu in education:
            dic[re.sub(r'\s*','',edu)] = 1 #有出现就把flag改为1
        for key, value in dic.items():
            if value == 1:  #找到最高学位
                return key
    else:
        return '' 


if __name__ == '__main__':
    pass