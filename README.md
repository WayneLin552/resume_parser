# resume_parser
resume_parser
1. 程序用途：
	本程序用于简历解析。
	解析的字段包括 姓名，性别，年龄，学历，学校，毕业时间，工作年限，专业，电话，教育经历，项目经历，工作经历，技能。
	目前支持的解析文件格式包括doc，docx，pdf ，暂不支持图片、html、excel等格式文件的解析。

2. 程序运行方式：
	2.1 程序默认每10min运行一次，用于更新并提取../docx_dics/resumes目录下新加入的简历，简历的全部解析结果导入在sunline_resume数据库中，上一次的解析结果在result文件目录中。
	2.2 hr可以手动操作立刻提取简历信息，使用方法：
	主程序运行的入口为 bin目录下的start.py,
	运行方式为在命令行输入： python start.py + 待解析的文件目录(默认../docx_dics/resumes) + 使用的系统(默认linux)
	例如 python start.py --path ../docx_dics/resumes --system win
	###########
	【--system】 可选项目:linux 或者 win
	linux指Linux系统，win指Windows系统，请根据所需正确填写，默认为linux系统。
	【--path】 若在默认子文件夹下(../docx_dics/resumes)可以填相对路径，否则要填绝对路径。
	###########
	###########
	【important！！】
	为了方便追溯简历投放的HR名字，建议将要解析的简历统一打包到同一个文件夹下，文件夹命名格式为：HR名字
	例如，HR小明需要解析4份简历，那么他需要将简历打包为如下：
		主文件夹： 		小明(HRname){
		主文件夹下文件：				简历1
							简历2
							简历3
							简历4
					    	    }
		并建议把此文件夹放在默认的../docx_dics/resumes目录下
	###########

3. 程序输出：
	输出文件包括：
	log 目录下的运行日志文件
	result 文件下上一次更新的简历中的结果文件:(若10min前没有新简历添加，将是空文档)：
		base_info_result.csv			储存基本资料字段
		edu_exp_info_result.csv			储存教育经历字段
		work_exp_info_result.csv		储存工作经历字段
		proj_exp_info_result.csv		储存项目经历字段
	程序每10min自动运行一次，将数据储存在sunline_resume数据库中
	##############
	云桌面MySQL数据库IP 10.22.86.17
	端口 3306
	数据库名称 sunline_resume
	用户名及密码请找相关管理员索取，用于提取简历解析结果
	##############
	

4. 文件目录简介：
	bin：程序主入口
	logconf: 配置文件，包括日志配置文件log_settings.py，用户配置文件config.ini
	core：程序核心代码，包括：主文件main.py, 各字段提取模块 *.extractor.py, insert to database module insert2db.sh
	db：数据库文件（暂无）
	docs_dics：程序所用的文本文件，包括：major_dic 学科专业字典，school_dic 学校字典等
	lib：自定义库（暂无）
	log：程序运行日志文件
	result：程序结果输出文件*.csv
	README.TXT: 程序说明文档
	requirements.txt: Python程序运行依赖包文档	

5. 程序运行效果：

	目前的解析识别率为：
556文件
平均2.18s		
准确度	        python	  software
name	        96%	      93%
age	        68%	      63%
gender	        70%	      68%
degree	        83%	      79%
graduate_time	93%	      94%
phone	        91%	      91%
email	        83%	      82%
school	        83%           86%
major	        77%	      73%
worktime	93%	      90%
skill	        61%	      66%
		
edu_date	75%	      86%
edu_school	83%	      86%
edu_major	77%	      73%
edu_degree	92%	      93%
		
work_company	88%	      74%
work_date	94%	      86%
work_position   86%	      77%
work_desc	81%	      65%

proj_name	78%		/
proj_data	85%		/
proj_role	93%		/
proj_desc	90%		/

