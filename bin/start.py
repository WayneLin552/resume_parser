#!/root/anaconda3/bin/python

import sys
import os
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

path = sys.argv[0]
# path = r'..\docs_dics\resumes'
# path = os.path.abspath(path)

from core import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Resumes Evaluation')
    parser.add_argument('--path', type=str,default=os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]+'/docs_dics/resumes')
    parser.add_argument('--system', type=str,default='linux')
    args = parser.parse_args()
    path = args.path
    path = os.path.abspath(path)
    main.total_extract(path,args.system)

    # import configparser
    # config = configparser.ConfigParser()
    # config.read(r'.\bin\conf.ini')
    # print(config['DEFAULT']['log_dir'])
    # config = configparser.ConfigParser()
    # config['DEFAULT'] = {'log_dir': '../log',
    #                      'output_dir': '../docs',
    #                      'db_user': '',
    #                      'db_password': '',
    #                      'db_lsn': ''}
    # with open('config.ini', 'w') as configfile:
    #     config.write(configfile)