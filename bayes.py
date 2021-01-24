# -*- coding: utf-8 -*-
# coder: oslijw

# 贝叶斯网络

# from sklearn.neural_network import MLPClassifier
# X = [[0., 0.], [1., 1.]]
# y = [0, 1]
# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
# clf.fit(X, y)
# print(clf.predict([[2., 2.], [1., 1.]]))
import pandas as pd
from collections import Counter
def bayes(data:pd.DataFrame, test:dict, label_name:str):
       labels = data[label_name]
       class_counter = dict(Counter(labels))
       class_prop = {key:int(value)/data.shape[0] for key,value in class_counter.items()}
       unique_label = list(class_prop.keys())
       final_class = ''
       final_prop = 0
       prop_dict = {}
       for label in unique_label:
              temp_data = data.where(data[label_name] == label).dropna(axis=0, how='any') # 筛选出来属于Ci的数据
              prop = 1
              for i in test.keys(): # 对每个属性遍历
                     col_prop = dict(Counter(temp_data[i]))[test[i]]/temp_data.shape[0]
                     # 假定类独立
                     prop = prop * col_prop
              prop = prop * class_prop[label]
              prop_dict[label] = prop
              if prop > final_prop:
                     final_class = label
                     final_prop = prop
       return final_class,final_prop,prop_dict

if __name__ == '__main__':
    data = pd.DataFrame(
        [{'age': 'young', 'income': 'high', 'student': 'no', 'credit_rating': 'fair', 'by_computer': 'no'},
         {'age': 'young', 'income': 'high', 'student': 'no', 'credit_rating': 'excellent', 'by_computer': 'no'},
         {'age': 'middle_aged', 'income': 'high', 'student': 'no', 'credit_rating': 'fair', 'by_computer': 'yes'},
         {'age': 'senior', 'income': 'medium', 'student': 'no', 'credit_rating': 'fair', 'by_computer': 'yes'},
         {'age': 'senior', 'income': 'low', 'student': 'yes', 'credit_rating': 'fair', 'by_computer': 'yes'},
         {'age': 'senior', 'income': 'low', 'student': 'yes', 'credit_rating': 'excellent', 'by_computer': 'no'},
         {'age': 'middle_aged', 'income': 'low', 'student': 'yes', 'credit_rating': 'excellent', 'by_computer': 'yes'},
         {'age': 'young', 'income': 'medium', 'student': 'no', 'credit_rating': 'fair', 'by_computer': 'no'},
         {'age': 'young', 'income': 'low', 'student': 'yes', 'credit_rating': 'fair', 'by_computer': 'yes'},
         {'age': 'senior', 'income': 'medium', 'student': 'yes', 'credit_rating': 'fair', 'by_computer': 'yes'},
         {'age': 'senior', 'income': 'medium', 'student': 'yes', 'credit_rating': 'excellent', 'by_computer': 'no'},
         {'age': 'middle_aged', 'income': 'high', 'student': 'yes', 'credit_rating': 'fair', 'by_computer': 'yes'},
         {'age': 'young', 'income': 'medium', 'student': 'yes', 'credit_rating': 'excellent', 'by_computer': 'yes'},
         {'age': 'middle_aged', 'income': 'medium', 'student': 'no', 'credit_rating': 'excellent',
          'by_computer': 'yes'}])
    test = {'age':'young',"income":'medium','student':'yes','credit_rating':'fair'}
    final_class, prop, _ = bayes(data,test,'by_computer')
    print(f'测试数据 : {test}\n贝叶斯分类结果为-->最终分类 : {final_class}, 概率: {prop}')




