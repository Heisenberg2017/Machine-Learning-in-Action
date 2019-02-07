# -*- coding:utf-8 -*-

'''
决策树
    * 计算熵和信息增益
    *
'''
from math import log


def calc_shannon_ent(data_set):
    '''
    计算香农熵
    :param data_set:
    :return:
    '''
    num_entries = len(data_set)
    label_counts = {}
    for feat_vec in data_set:
        current_label = feat_vec[-1]
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key, value in label_counts.items():
        prob = float(value) / num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent

def create_data_set():
    '''
    构建初始数据集
    :return:
    '''
    data_set = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'], 
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return data_set, labels


def split_data_set(data_set, axis, value):
    '''
    获取axis列值为value的数据子集
    :param data_set:
    :param axis:
    :param value:
    :return:
    '''
    ret_data_set = []
    for feat_vec in data_set:
        if feat_vec[axis] == value:
            reduced_feat_vec = feat_vec[:axis]
            reduced_feat_vec.extend(feat_vec[axis+1:])
            ret_data_set.append(reduced_feat_vec)
    return ret_data_set


def choose_best_feature_to_split(data_set):
    '''
    选出数据集中信息增益最大的值
    :param data_set:
    :return:
    '''
    num_features = len(data_set[0]) - 1
    base_entropy = calc_shannon_ent(data_set)
    base_info_gain = 0.0; best_feature = -1
    for i in range(num_features):
        feat_list = [example[i] for example in data_set]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = split_data_set(data_set, i, value)
            prob = len(sub_data_set) / float(len(data_set))
            new_entropy += prob * calc_shannon_ent(
                sub_data_set)
        info_gain = base_entropy - new_entropy
        if (info_gain > base_info_gain):
            base_info_gain = info_gain
            base_feature = i
    return base_feature




if __name__ == '__main__':
    my_data, my_label = create_data_set()
    # print my_data
    # print calc_shannon_ent(my_data)
    # my_data[0][-1] = 'maybe' 
    # print my_data
    # print calc_shannon_ent(my_data)
    # print split_data_set(my_data, 0, 0)
    # print split_data_set(my_data, 0, 1)
    # print split_data_set(my_data, 1, 0)
    # print split_data_set(my_data, 1, 1)
    # 获取信息增益最大的特征
    print choose_best_feature_to_split(my_data)