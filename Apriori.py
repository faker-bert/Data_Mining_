# -*- coding: utf-8 -*-
# coder: oslijw
# blog : https://oslijw.github.io/

# 实现最基础的频繁项集挖掘算法Apriori
from collections import Counter
from itertools import combinations

records = [['I1','I2','I5'],
              ['I2','I4'],
              ['I2','I3'],
              ['I1','I2','I4'],
              ['I1','I3'],
              ['I2','I3'],
              ['I1','I3'],
              ['I1','I2','I3','I5'],
              ['I1','I2','I3']]

def status(wait, forbid):
   # 为True 的时候说明这个等待判断的记录包含在之前的不可用模式中不用计数
    return all([True  if i in wait else False for i in forbid.split(';')])

def candidate(_dict):
    '''
    :param _dict: 键名为字符串 键值为计数
    :return: 候选集-->字符串列表 分隔符为;
    '''
    # 根据前一步的频繁集结果进行拼接 生成多个候选集
    _list = []
    keys = list(_dict.keys())
    # print(keys)
    len_keys = len(keys)
    for i in range(len_keys):
        for j in range(i+1, len_keys): # 这样就不会出现两个重复的在一起 所以不需要使用set
            # 先得到一个列表 在使用另外的进行拼接 使用set 避免重复
            code = keys[i].split(';')
            code.extend(keys[j].split(';'))
            # 保持某一顺序即可 --> 判断出现的code里面是否已经在_list中
            flag = any([status(";".join(code),i) for i in _list])
            if not flag:
                _list.append(";".join(set(code)))
    return _list


def APRIORI(records, support):
    print(f'基于数据集 \n{records}\n寻找支持度为 {support} 的频繁集'
          f'\n===============================================================================')
    # 将传递进来的记录集平坦化
    out_fp = []
    record = [i for record in records for i in record]
    forbid = [] # 存放不可能为频繁集的子集 用于排除
    temp_dict = {key:value for key,value in dict(Counter(record)).items() if value >= support}
    forbid.extend({key: value for key, value in dict(Counter(record)).items() if value < support}.keys())
    # 筛选合适的一元频繁集 --> 由于这边一元频繁集不可能是所谓的关联规则, 所以这边并不考虑
    # 然后依次进行连接 使用set存放 达到自动去重的目的 然后进records扫描 并通过阈值进行筛选 同时加入输出频繁集
    while True:
        _dict = {} # 用来存放每次得到的候选集计数
        # print(_dict)
        _list = candidate(temp_dict)  # 获得候选集
        if _list: # 如果只有一个就不进行拼接 从而返回空列表也不进入
            # 还需要筛选得到下一个级别的候选集
            print(f'存在候选集 {_list} 继续执行....')
            # print(f'初始候选集为空')
            for _record in records:
                # print(_record)
                # 循环记录并循环候选集以得到候选集-->由于字典的键不能为列表,所以这边转化为字符串
                for candi in _list: # 从中选取一个出来筛选
                    flag = any([status(candi,i) for i in forbid]) # 初步判断是否为可用频繁模式 为True 那么说明发现了包含之前的子模式
                    contain_flag = all([True if c in _record else False for c in candi.split(';')])  # 判断是否可加
                    # print(f'{candi}--{_record}')
                    if contain_flag and not flag:
                        # print(f'{candi}--{_record}')
                        if candi not in _dict.keys(): # 这边可能会出现乱序的情况 需要处理
                            _dict[candi] = 1
                        else:
                            _dict[candi] = _dict[candi] + 1
                        # print(_dict)
                        # print('------')
            # 获得满足支持度的候选集 也就是一次循环中的频繁集
            # breakpoint()
            # print(f'候选集为{_dict}')
            forbid = []
            forbid.extend({key: value for key, value in _dict.items() if value < support}.keys()) # 可以使其每次刷新
            temp_dict = _dict = {key: value for key, value in _dict.items() if value >= support}
            # 剔除非频繁集 --> 当非频繁集出现在某个模式中 那么直接跳过

            out_fp.append(temp_dict) # 存储到输出中等待输出
            print(f'某一次的频繁集为 : {_dict}')
            print('-------------------------------------------------------------------------------')
        else:
            print('====>获得全部频繁集完毕')
            break
    out_fp = [i for i in out_fp if i]
    print(f'===============================================================================\n最终频繁集为 {out_fp}')
            # breakpoint()
    return out_fp

def frequency_rule(out_fp, confidence, records):
    '''

    :param out_fp: 传入频繁模式
    :param confidence: 置信度
    :param records: 数据集
    :return: 返回频繁规则 以及对应的置信度
    '''
    print('===============================================================================')
    print(f'基于频繁集,寻找置信度为{confidence}的规则')
    left = []
    right = []
    temp_left = []
    temp_right = []
    maybes = [s.split(';') for i in out_fp for s in i.keys()] # 先获得所有可能的集 列表-->同时out_fp的次数
    # 每个模式下 都会有很多的规则前项 主要得到规则前项即可 因为计算公式并不需要规则后项
    for maybe in maybes:
         # 一个模式
        for i in range(1, len(maybe)+1):
            # 计算多模式下的规则前项
            sons = [s for s in combinations(maybe, i) if len(s) != len(maybe)]
            dat = list(set(maybe) - set(son) for son in sons)
            temp_left.extend(sons)
            temp_right.extend(dat)
        left.append(temp_left) # 每种频繁模式都会在其中
        right.append(temp_right)
        temp_left = []
        temp_right= []
    # 得到的left 和right 均为二维列表形式
    counter = {}
    for record in records:
        # 获得所有的规则前项 计次
        # 对每个记录都判断一下是否存在
        for i in range(len(left)):
            # 针对每个示例
            for j in range(len(left[i])):
                # 针对每个模式下的子模式 也就是规则前项
                # 优化方法取set
                flag = all([True if z in record else False for z in left[i][j]])
                # 判断子模式是否在其中
                if flag:
                    if  f'{i}-{j}' in counter:
                        counter[f'{i}-{j}'] = counter[f'{i}-{j}'] + 1
                    else:
                        counter[f'{i}-{j}'] = 1
    # print(counter)
    pattern_count = [s for i in out_fp for s in i.values()]
    pattern = [s for i in out_fp for s in i.keys()]
    for i in range(len(left)):
        for j in range(len(left[i])):
            count = pattern_count[i]/counter[f'{i}-{j}']
            if count > confidence:
                print(f"pattern: {pattern[i]}      pattern_count: {pattern_count[i]}      {';'.join(left[i][j])}  count: " + str(counter[f'{i}-{j}']))
                # 打印出来
                print(f'发现规则:  {";".join(left[i][j])}->{";".join(right[i][j])}   confidence:{count}')
                print('-------------------------------------------------------------------------------')

fp = APRIORI(records,2)
frequency_rule(fp, 0.5, records)

