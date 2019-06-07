# -*- coding: utf-8 -*-

# import csv
# import sys
# import codecs


# # csv.field_size_limit(sys.maxsize)
# # htmllines = codecs.open('./碩士/102學年度碩士班/榜單公告.htm','r',encoding='utf-8', errors='ignore').readlines()
# # for line in htmllines:
# #     print (line)



#import bs4
import sys
import os
import re
import time
import json
#import mechanize
from bs4 import BeautifulSoup

import requests


#import urllib2    

url = "http://www.ncku.edu.tw/~register/chinese/success/103ssm.htm"
response = requests.get(url)
print (response)
response.encoding = 'big5'

soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('td')
n=7

for name in enumerate(articles):
	# print (name)
	# print (len(str(name[1]).split(" ")))
	name_list = str(name[1]).split(" ")
	print (name)
	print (len(name_list))

	output = ""

	if(len(name_list)==n-2 or len(name_list)==n or len(name_list)==n+2):
	#4 
		output = name_list[2]
		if(name_list[len(name_list)-1]=="(職)</td>"):
			output+=" 職"
		print (output)
	# 	output+=" 職"
	# if(len(name_list)==n):
	# #3 
	# 	print (name_list[2])
	# if(len(name_list)==n+2):
	# #2
	# 	print (name_list[2]+"!!")



	# if(len(str(name[1]).split(" "))==19):
	
	# 	print (str(name[1]).split(" ")[3])