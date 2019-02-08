# -*- coding:utf-8 -*-

'''
决策树
    * 计算熵和信息增益
    * 多数表决法
    * 绘制树形图
    * 使用决策树预测隐形眼镜类型
'''
import operator
from math import log
import tree_plotter


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
        if current_label not in label_counts:
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


def majority_cnt(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count:
            class_count[vote] = 0
        class_count += 1
    sorted_class_count = sorted(class_count.iteritems(),
                                key=operator.itemgetter(1),
                                reverse=True)
    return sorted_class_count[0][0]


def create_tree(data_set, labels):
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    if len(data_set[0]) == 1:
        return majority_cnt(class_list)
    best_feat = choose_best_feature_to_split(data_set)
    best_feat_label = labels[best_feat]
    my_tree = {best_feat_label: {}}
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in data_set]
    unique_vals = set(feat_values)
    for value in unique_vals:
        sub_labels = labels[:]
        my_tree[best_feat_label][value] = create_tree(
            split_data_set(data_set, best_feat, value), sub_labels)
    return my_tree


def classify(input_tree, feat_labels, test_vec):
    first_str = input_tree.keys()[0]
    print first_str
    second_dict = input_tree[first_str]
    print second_dict
    feat_index = feat_labels.index(first_str)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]

    return class_label


def store_tree(input_tree, filename):
    import pickle
    with open(filename, 'w') as fw:
        pickle.dump(input_tree, fw)


def grab_tree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


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
    # print choose_best_feature_to_split(my_data)
    # 创建一颗决策树
    # _, labels = create_data_set()
    # my_tree = tree_plotter.retrieve_tree(0)
    # print classify(my_tree, labels, [0, 0])
    # print classify(my_tree, labels, [1, 1])
    # store_tree(my_tree, 'classifier_storage.txt')
    # print grab_tree('classifier_storage.txt')
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lenses_labels = ['age', 'prescript', 'astigmatic', 'tear_rate']
    lenses_tree = create_tree(lenses, lenses_labels)
    print lenses_tree
    tree_plotter.create_plot(lenses_tree)