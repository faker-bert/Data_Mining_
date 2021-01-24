# -*- coding: utf-8 -*-
# coder: oslijw
# blog : https://oslijw.github.io/

import numpy as np
import pandas as pd

# 正常而言都会对缺失值进行处理, 所以基本全部的指示符均为1
col_type = {'Nominal': 0, 'Ordinal': 1, 'Numerical': 2}
list_data = [['A', '优秀', 45], ['B', '一般', 22], ['C', '好', 64], ['A', '优秀', 28]]
df_matrix = pd.DataFrame(list_data)
rf = [{'一般': 1, '好': 2, '优秀': 3}]


def get_nominal_diff(nominal_df):
    obj_num = nominal_df.shape[0]
    try:
        nominal_matrix = np.zeros((obj_num, obj_num))
        # 初始化零矩阵
        col = nominal_df.shape[1]
    except:
        col = 1
    for i in range(obj_num):
        for j in range(i + 1, obj_num):
            row1 = nominal_df.iloc[i]
            row2 = nominal_df.iloc[j]
            for num in range(col):
                if row1[num] != row2[num]:
                    nominal_matrix[i, j] = nominal_matrix[i, j] + 1
                    nominal_matrix[j, i] = nominal_matrix[i, j]
    # print(nominal_matrix)
    return nominal_matrix


# get_nominal_diff(df_matrix.iloc[:,col_type['Nominal']])

def get_numerical_diff(numerical_df):
    obj_num = numerical_df.shape[0]
    try:
        numerical_matrix = np.zeros((obj_num, obj_num))  # 初始化零矩阵
        col = numerical_df.shape[1]
    except:
        col = 1
    # 否则会变成一维数组
    # 0 是列
    _range_max = np.array(numerical_df).reshape(obj_num, col).max(axis=0)
    _range_min = np.array(numerical_df).reshape(obj_num, col).min(axis=0)
    _range = _range_max - _range_min
    for i in range(obj_num):
        for j in range(i + 1, obj_num):
            row1 = numerical_df.iloc[i]
            row2 = numerical_df.iloc[j]
            try:
                size = row1.shape[0]
            except:
                size = 1
            for num in range(size):
                if size != 1:
                    numerical_matrix[i, j] = numerical_matrix[i, j] + abs(row1[num] - row2[num]) / _range[num]
                    numerical_matrix[j, i] = numerical_matrix[i, j]
                else:
                    numerical_matrix[i, j] = numerical_matrix[i, j] + abs(row1 - row2) / _range[num]
                    numerical_matrix[j, i] = numerical_matrix[i, j]
    return numerical_matrix


# get_numerical_diff(df_matrix.iloc[:,col_type['Numerical']])
def get_ordinal_diff(ordinal_df, rf_list):
    # 首先数值化,然后用数值计算函数计算
    ordinal_df = pd.DataFrame(ordinal_df)
    obj_num = ordinal_df.shape[0]
    try:
        col = ordinal_df.shape[1]
    except:
        col = 1
    for row in range(obj_num):
        for att in range(col):
            _dict = rf_list[att]
            ordinal_df.iloc[row, att] = _dict[ordinal_df.iloc[row, att]]
    _range_max = np.array(ordinal_df).reshape(obj_num, col).max(axis=0)
    _range = _range_max - 1
    for row in range(obj_num):
        for attr in range(col):
            ordinal_df.iloc[row, att] = (ordinal_df.iloc[row, att] - 1) / _range[attr]
    # print(ordinal_df)
    return ordinal_df


# get_ordinal_diff(df_matrix.iloc[:,col_type['Ordinal']],[{'一般':1,'优秀':2,'好':3}])


def run(df, col_type):
    df_matrix.iloc[:, col_type['Ordinal']] = get_ordinal_diff(df_matrix.iloc[:, col_type['Ordinal']], rf)
    Numerical = get_numerical_diff(df_matrix.iloc[:, col_type['Numerical']])
    Ordinal = get_numerical_diff(df_matrix.iloc[:, col_type['Ordinal']])
    Nominal = get_nominal_diff(df_matrix.iloc[:, col_type['Nominal']])
    print((Nominal + Ordinal + Numerical) / df.shape[1])

if __name__ == '__main__':
    run(df_matrix, col_type)

