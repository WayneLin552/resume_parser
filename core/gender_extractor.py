#!/root/anaconda3/bin/python
import re

def gender_extract(text):
    '''
    获取性别

    Parameters
    ----------
    text: string
        简历解析后的文本

    Returns: string
    -------
        性别 / ''
    '''    
    
    #print(text)
    gender = re.search(r"男|女", text)
    if gender:
        return gender.group()
    else:
        return ''   
            
if __name__ == '__main__':
    pass