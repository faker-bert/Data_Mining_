# -*- coding: utf-8 -*-
# coder: oslijw
import random
import scipy.spatial.distance as dist
import numpy as np
dataSet = np.array([[1, 2], [2, 2], [2, 3],
           [8, 7], [8, 8], [25, 80]])
def DBSCAN(dataSet, radius, MinPts):
    noise = []
    dist_list = dist.pdist(dataSet, metric='euclidean')
    dist_matrix = np.array(dist.squareform(dist_list))
    visit_list = [0 for _ in range(len(dataSet))] # 当对应索引为0 的时候说明其为unvisited对象
    cluster = {}
    count = 0
    finish = []
    while list(np.where(np.array(visit_list) == 0)[0]): # 当节点全被标记为visited 那么结束循环
        print('迭代...')
        init_p = random.sample(range(len(visit_list)), 1)[0] # 随机选择一个作为p
        while visit_list[init_p] == 1:
            print('init点已被初始化过 重新随机...')
            init_p = random.sample(range(len(visit_list)), 1)[0]
        visit_list[init_p] = 1
        if np.sum((dist_matrix[:,init_p] < radius) != 0) >= MinPts:
            # 当radius半径内个数超过MinPts 则说明p非噪声
            cluster[count] = [] # 创建新簇
            cluster[count].append(init_p) # 将满足条件的节点加入簇中
            N = []
            N.extend(list(np.where([dist_matrix[:,init_p] < radius])[1]))
            for index in N:
                if visit_list[index] == 0 :
                    visit_list[index] = 1
                    if np.sum((dist_matrix[:,index] < radius) != 0) >= MinPts:
                        N.extend(list(np.where([dist_matrix[:, index] < radius])[1]))
                        N = list(set(N))

                        [finish.extend(i) for i in cluster.values()]
                    finish = list(set(finish))
                    if index not in finish:
                        cluster[count].append(index)
            print(f'目前簇结果 : {cluster}')
            count = count + 1
        else:
            print(f'{init_p} 记录为噪声')
            noise.append(init_p)
    return noise,cluster
if __name__ == '__main__':
    noise, cluster = DBSCAN(dataSet, 3, 2)
    print(noise, cluster)



