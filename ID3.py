# -*- coding: utf-8 -*-
# coder: oslijw

import numpy as np
from collections import Counter

def clacShannonEnt(dataSet):
    labelCount = np.array(list(Counter(dataSet[:,-1]).values()))
    prop = labelCount/np.sum(labelCount)
    shannonEnt = -sum(prop/np.log2(prop))
    return shannonEnt

def splitDataSet(dataSet:np.array, col:int, value:str)->np.array:
    retDataSet = np.empty((np.shape(dataSet)[1]-1),dtype = np.float64)
    for dataRow in dataSet:
        # 为了方便比较将数据类型全部转化成str
        if str(dataRow[col]) == str(value):
            retDataSet = np.row_stack((retDataSet,np.delete(dataRow,int(col),axis=0))) # 0代表列
    retDataSet = retDataSet[1:,]
    return retDataSet

def choose_best_feature(dataSet:np.array)->int:
    # 这边减1是由于最后一列实际上是分类而非真实的特征
    feature_num = np.shape(dataSet)[1]-1
    base_entropy = clacShannonEnt(dataSet)
    best_Infogain = 0.0
    best_Feature = -1
    for i in range(feature_num):
        unique_values = set(dataSet[:,i])
        feature_split_entropy = 0
        for unique_value in unique_values:
            subData = splitDataSet(dataSet,col=i,value=unique_value)
            # 计算权重
            prob = len(subData)/len(dataSet)
            feature_split_entropy += prob * clacShannonEnt(subData)
        infoGain = base_entropy - feature_split_entropy
        if infoGain>best_Infogain:
            best_Infogain = infoGain
            best_Feature = i
    return best_Feature

def get_majority_label(dataSet:np.array):
    # 这边只有一列
    label_counts = Counter(dataSet[:,0])
    return label_counts.most_common(1)[0][0]

def create_tree(dataSet: np.array, features: list) -> dict:
    classCount = dataSet[:, -1]
    # 递归终止条件1
    if len(set(classCount)) == 1:
        return set(classCount).pop()
    # 递归终止条件2
    if np.shape(dataSet)[1] == 1:
        return get_majority_label(dataSet)

    bestFeatureNum = choose_best_feature(dataSet)

    bestFeature = features[bestFeatureNum]
    myTree = {bestFeature: {}} # 精华

    uniqueValues = set(dataSet[:, bestFeatureNum])
    for value in uniqueValues:
        subFeatures = features[:]
        # 在python中,会传递引用,所以这边需要使用切片来建立副本
        myTree[bestFeature][value] = create_tree(splitDataSet(dataSet, col=bestFeatureNum, value=value), subFeatures)
    return myTree

def create_data():
    data_set = np.array([[1,1,1,'a'],
                            [1,1,1,'ab'],
                            [1,0,0,'a'],
                            [0,1,1,'no'],
                            [0,1,0,'no']])
    label = ['no surfacing','flippers','asb']
    return data_set,label

if __name__ == '__main__':
    data_set, label = create_data()
    ID3 = create_tree(data_set,label)
    print(ID3)
