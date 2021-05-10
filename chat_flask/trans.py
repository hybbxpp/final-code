
'''
Author: hybb
Email: sc17zz@leeds.ac.uk
File: __init__.py
Aim: data cleaning
'''

import json
a = []
with open('trans.txt', 'r', encoding='utf-8-sig') as fp:
     data_list = fp.readlines()
for i in data_list:
    i = i.rstrip("\n")
    a.append(i)
regexp_name = ''
num = 0
with open('data.json', 'r', encoding='utf-8-sig', errors='ignore') as fp:
    data_list = fp.readlines()
data_list = [json.loads(item) for item in data_list]
with open('over.json', 'w', encoding='utf-8-sig') as fp:
    for item in data_list:
        if item['通用名称'] in a:
            num+=1
            a.remove(item['通用名称'])
            fp.write(str(item)+'\n')
# with open('over.txt', 'w', encoding='utf-8-sig') as fp:

print(num)