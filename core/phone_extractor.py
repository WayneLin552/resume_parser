#!/root/anaconda3/bin/python

import re

def phone_extract(text):
    """
    获取手机号

    Parameters
    ----------
    text: string
        简历解析后的文本

    Returns: string
    -------
        手机号 / ''
    """
    
    phone = ""
    # 直接通过文件名查找
    # file_name = re.split(r"/+|\\+", self.file_dir)[-1]
    # number = re.findall(r"\d{11,13}", file_name)
    # if len(number) > 0 and re.search(r"^1", number[0]):
    #     phone = number[0]
    #else:
        
    # 通过关键词查找
    for line in re.split(r"[\n\s]+", text):
        if "电话" in line or "手机" in line:
            line = re.sub(r"[()（）：:+\-]", "", line)
            try:                    #我改的地方
                number = re.findall(r"\d{11,13}", line)[0]
                phone = re.sub(r"^(86)", "", number)  
                return phone        #我改的地方
            except:                 #我改的地方
                continue            #我改的地方
    # 直接通过数字长度查找
    if phone == "":
        text = re.sub(r"[()（）+\-]", "", text)
        phones = re.findall(r"\d{11,13}", text)
        phones = [re.sub(r"^(86)", "", p) for p in phones if re.search(r"^1", re.sub(r"^(86)", "", p))]
        phone = ",".join(set(phones))
    return phone

if __name__ == '__main__':
    pass