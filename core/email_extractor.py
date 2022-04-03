#!/root/anaconda3/bin/python
# -*- coding: utf-8 -*-
import re

#def email_extract(full_words):
    # """
    # 获取邮箱

    # Parameters
    # ----------
    # text: string
    #     简历解析后的文本

    # Returns: string
    # -------
    #     邮箱 / ''
    # """
    
    # email = ""
    # for word in full_words:
    #     text = word["text"]
    #     if "@" in text and "." in text:
    #         for e in re.findall(r"[a-zA-Z0-9_\-.@]+", text):
    #             if "@" in e:
    #                 email = e
    #                 break
    #     if email != "":
    #         break
    # return email
    

def email_extract(text):
    """
    获取邮箱

    Parameters
    ----------
    text: string
        简历解析后的文本

    Returns: string
    -------
        邮箱 / ''
    """
    
    email = ""
    lines = [i for i in re.split(r'\n',text) if re.search(r'[0-9A-Za-z\u4e00-\u9fa5]',i)] 
    for line in lines:
        if "@" in text and "." in line:
            for e in re.findall(r"[a-zA-Z0-9_\-.@]+", line):
                if "@" in e:
                    email = e
                    break
        if email != "":
            break
    return email
    
if __name__ == '__main__':
    pass