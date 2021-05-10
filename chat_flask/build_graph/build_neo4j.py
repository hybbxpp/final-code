#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''                                                                                                             
Author: hybb
Email: sc17zz@leeds.ac.uk
File: __init__.py
'''


import json
from py2neo import Relationship, Node
from xwtools.neo4j_op import Neo4jOp

op_neo4j = Neo4jOp(label='neo4j') #覆盖原有图谱
op_neo4j.truncate_neo4j() #清空图谱并重建


def create_graph(item, key_1, key_2, relation_name):
    if item.get(key_1) and item.get(key_2):
        # 创建节点1
        node_1 = op_neo4j.nodes_match(key_1, _id=item[key_1])
        if not node_1:
            node_1 = Node(key_1, name=item[key_1], _id=item[key_1])

        # 创建节点2
        node_2 = op_neo4j.nodes_match(key_2, _id=item[key_2])
        if not node_2:
            node_2 = Node(key_2, name=item[key_2], _id=item[key_2])

        # 创建两个节点间的关系
        relation = Relationship(node_1, relation_name, node_2)
        op_neo4j.create(relation)


# ['通用名称', '商品名称', '主要成份', '性状', '功能主治', '规格', '用法用量', '不良反应',
#        '禁忌', '注意', '药物相互作用', '贮藏', '包装规格', '有效期', '批准文号', '生产企业', '执行标准',
#        '英文名称', '适应症', '药理毒理', '药代动力学', '孕妇及哺乳期妇女用药', '儿童用药', '老人用法', '药物过量',
#        '类别', '警告', '临床研究']
def write_data_to_neo4j(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
        data_list = fp.readlines()
    data_list = [json.loads(item) for item in data_list]
    num = 0
    for item in data_list[:10000]:
        num += 1
        print(item)
        #print(num)
        create_graph(item, '通用名称', '主要成份', '主要成份')
        create_graph(item, '通用名称', '性状', '性状')
        create_graph(item, '通用名称', '功能主治', '主治功能')
        create_graph(item, '通用名称', '用法用量', '用法用量')
        create_graph(item, '通用名称', '不良反应', '不良反应')
        create_graph(item, '通用名称', '有效期', '有效期')
        create_graph(item, '通用名称', '生产企业', '生产商')
        create_graph(item, '通用名称', '贮藏', '贮藏方式')
        create_graph(item, '通用名称', '注意', '注意')
        create_graph(item, '通用名称', '包装规格', '规格')
        create_graph(item, '通用名称', '批准文号', '批准文号')
        create_graph(item, '通用名称', '适应症', '适应症')
        create_graph(item, '通用名称', '孕妇及哺乳期妇女用药', '孕妇用药')
        create_graph(item, '通用名称', '儿童用药', '儿童用药')
        create_graph(item, '通用名称', '老人用法', '老人用法')
        create_graph(item, '通用名称', '药物过量', '药物过量')
        create_graph(item, '通用名称', '临床研究', '临床研究')


def build_entity_relation_regexp(file_path, out_file):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
        data_list = fp.readlines()
    data_list = [json.loads(item) for item in data_list]
    name_list = [item['通用名称'] for item in data_list]
    regexp_name = '|'.join(name_list)
    with open(out_file, 'w', encoding='utf-8') as fp:
        fp.write(regexp_name)

def build_entity_relation_database(file_path, out_file):
    with open(file_path, 'r', encoding='utf-8') as fp:
        whole = ""
        data_list = fp.readlines()
        data_list = [json.loads(item) for item in data_list]
        print(data_list)
    for item in data_list:
        name = item['通用名称']
        contains = item['主要成份']
        contains2 = item['性状']
        contains3 = item['功能主治']
        contains4 = item['用法用量']
        contains5 = item['不良反应']
        contains6 = item['有效期']
        contains7 = item['贮藏']
        contains8 = item['注意']
        contains9 = item['包装规格']
        contains11 = item['批准文号']
        contains12 = item['适应症']
        contains13 = item['孕妇及哺乳期妇女用药']
        contains14 = item['儿童用药']
        contains15 = item['药物过量']
        contains16 = item['临床研究']
        contains17 = item['老人用法']
        contains18 = item['生产企业']
        seq=(name, contains, contains2,contains3,contains4,contains5,contains6,contains7,contains8,contains9,contains11,contains12,contains13,contains14,contains15,contains16,contains17,contains18)
        whole += ';'.join(seq)

    with open(out_file, 'w', encoding='utf-8') as fp:
        fp.write(whole)

if __name__ == '__main__':
    write_data_to_neo4j('./data/data.json')
    build_entity_relation_regexp('./data/data.json', './data/regexp_name.txt')
    #build_entity_relation_database('./data/data.json', './data/wtf.txt')
