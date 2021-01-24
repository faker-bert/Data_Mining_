# -*- coding: utf-8 -*-
# coder: oslijw
# blog : https://oslijw.github.io/

# Python实现PCA
# 在数据收集中,很多变量之间存在相关性,实际上会导致一定的维度冗余
# PCA就可以使得源数据以尽可能小的维度来描述,并且不会损失太多的信息

import numpy as np

def pca(x: np.ndarray, k: int) -> np.ndarray:
    '''
    PCA计算
    :param x: 传入原始矩阵
    :param k: 需要获得的主成分维度数量.也就是主成分个数
    :return: 返回计算得到的主成分
    '''
    obj_num, dim = x.shape
    if k > dim + 1:
        k = dim
    mean_vector = np.mean(x, axis=0)
    x = x - mean_vector
    cov_matrix = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            cov_matrix[i, j] = np.mean(x[:, i] * x[:, j]) - np.mean(x[:, i]) * np.mean(x[:, j])
            # 可以基于对称性优化计算过程
    eigenvalue, feature_vector = np.linalg.eig(cov_matrix)
    rank = np.argsort(-eigenvalue)
    get_k_index = rank[:k]
    vector_matrix = feature_vector[:, get_k_index]
    return np.dot(x, vector_matrix)

if __name__ == '__main__':
    original_matrix = np.array(
        [2.5, 2.4, .5, .7, 2.2, 2.9, 1.9, 2.2, 3.1, 3, 2.3, 2.7, 2, 1.6, 1, 1.1, 1.5, 1.6, 1.1, .9]).reshape([10, 2])
    print(pca(original_matrix, 1))
