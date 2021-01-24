# -*- coding: utf-8 -*-
# coder: oslijw

import numpy as np
import random
import math
import operator
dataset = [[1, 2], [1, 4], [1, 0],
       [4, 2], [4, 4], [4, 0]]
print(dataset)
def _eucliDist(A,B):
    return math.sqrt(sum([(a - b)**2 for (a,b) in zip(A,B)]))

def judge2(_list,dict2):
    for __, value2 in dict2.items():
        index2 = [i[0] for i in value2]
        if operator.eq(_list, index2):
            return True
    return False
def judge(dict1,dict2):
    for _,value1 in dict1.items():
        index1 = [i[0] for i in value1]
        if not judge2(index1,dict2):
            return False
        else:
            continue
    return True

def KMeans(dataset, k):
    centroid = [dataset[i] for i in random.sample(range(len(dataset)), k)] # 定序排序 会比较有好处
    print(f'初始化质心为{centroid}')
    cluster_result = {} # 存放最后结果
    while True: # 实际上是迭代次数,由于未知所以使用True
        temp_cluster_result = {} # 临时结果用于比对 验证是否收敛完成
        for index_dataSet, record in enumerate(dataset): # 对每个数据对象进行计算
            cluster = -1 # 临时聚类结果设为-1
            eucliDist = -1 # 用于设置欧式距离 比较替换
            for index_centroid, i in enumerate(centroid): # 求record 数据对象与每个质心的位置关系
                print(f'计算{record}和{i}的欧式距离')
                temp_eucliDist = _eucliDist(record, i) # 计算record 与某个质心的欧式距离
                if temp_eucliDist < eucliDist or eucliDist == -1: # 选择更小的作为质心
                    eucliDist = temp_eucliDist
                    cluster = index_centroid
            if cluster not in temp_cluster_result.keys():
                temp_cluster_result[cluster] = [(index_dataSet, record)]
            else:
                temp_cluster_result[cluster].append((index_dataSet, record))
            # temp_cluster_result.append(temp_cluster) # 将质心分类 存入临时结果
        if judge(temp_cluster_result,cluster_result): # 判断是否收敛完毕 亦可使用质心是否发生变化来确认
            # 利用temp_cluster_result取索引,对应于cluster_result 如果cluster_result只有一个值那么说明聚类结果一样
            print('聚类完成....')
            return centroid,temp_cluster_result
        else:
            print('未完全收敛,继续迭代....')
            cluster_result = temp_cluster_result
            # 运行这边 说明并未收敛完成 刷新质心
            centroid = []
            for _,value in cluster_result.items():
                cluster_data = np.array([i[1] for i in value])
                centroid.append(np.mean(cluster_data, axis=0))

centroid,clusters = KMeans(dataset,2)
print(f'聚类结果 : {clusters}\n聚类质心 : {centroid}')



