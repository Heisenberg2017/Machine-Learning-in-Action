# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt

decision_node = dict(boxstyle='sawtooth', fc='0.8')
leaf_node = dict(boxstyle='round', fc='0.8')
arrow_args = dict(arrowstyle='<-')


def plot_node(axl, node_txt, center_pt, parent_pt, node_type):
    axl.annotate(
        node_txt, xy=parent_pt, xycoords='axes fraction',
        xytext=center_pt, textcoords='axes fraction',
        va='center', ha='center', bbox=node_type,
        arrowprops=arrow_args
    )

#
# def simple_create_plot():
#     fig = plt.figure(1, facecolor='white')
#     fig.clf()
#     axl = plt.subplot(111, frameon=False)
#     plot_node(axl, 'decision node', (0.5, 0.1), (0.1, 0.5), decision_node)
#     plot_node(axl, 'leaf node', (0.8, 0.1), (0.3, 0.8), leaf_node)
#     plt.show()


def get_num_leafs(my_tree):
    num_leafs = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1
    return num_leafs


def get_tree_depth(my_tree):
    max_depth = 0
    first_str = my_tree.keys()[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def retrieve_tree(i):
    list_of_trees = [
        {'no surfacing': {
            0: 'no', 1: {
                'flippers': {0: 'no', 1: 'yes'}}}},
        {'no surfacing': {
            0: 'no', 1: {
                'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'yes'}}}},
    ]
    return list_of_trees[i]


def plot_mid_text(axl, cntr_pt, parent_pt, txt_string):
    x_mid = (parent_pt[0] - cntr_pt[0]) / 2.0 + cntr_pt[0]
    y_mid = (parent_pt[1] - cntr_pt[1]) / 2.0 + cntr_pt[1]
    axl.text(x_mid, y_mid, txt_string)


def plot_tree(axl, my_tree, parent_pt, node_txt, plot_info):
    num_leafs = get_num_leafs(my_tree)
    depth = get_tree_depth(my_tree)
    first_str = my_tree.keys()[0]
    cntr_pt = (plot_info['x_off'] +
               (1.0 + float(num_leafs)) / 2.0 / plot_info['total_w'],
               plot_info['y_off'])
    plot_mid_text(axl, cntr_pt, parent_pt, node_txt)
    plot_node(axl, first_str, cntr_pt, parent_pt, decision_node)
    second_dict = my_tree[first_str]
    plot_info['y_off'] = plot_info['y_off'] - 1.0 / plot_info['total_d']
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(axl, second_dict[key], cntr_pt, str(key), plot_info)
        else:
            plot_info['x_off'] = plot_info['x_off'] + 1.0 / plot_info['total_w']
            plot_node(axl, second_dict[key], (plot_info['x_off'],
                                              plot_info['y_off']),
                      cntr_pt, leaf_node)
            plot_mid_text(axl, (plot_info['x_off'], plot_info['y_off']),
                          cntr_pt, str(key))
    plot_info['y_off'] = plot_info['y_off'] + 1.0 / plot_info['total_d']


def create_plot(in_tree):
    '''
    绘制决策树
    :param in_tree:
    :return:
    '''
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    axl = plt.subplot(111, frameon=False, **axprops)
    plot_info = dict(
        total_w=float(get_num_leafs(in_tree)),
        total_d=float(get_tree_depth(in_tree)),
        x_off=-0.5 / float(get_num_leafs(in_tree)),
        y_off=1.0
    )
    plot_tree(axl, in_tree, (0.5, 1.0), '', plot_info)
    plt.show()


if __name__ == '__main__':
    # create_plot()
    # print retrieve_tree(1)
    tree0 = retrieve_tree(0)
    # print get_num_leafs(tree0)
    # print get_tree_depth(tree0)
    # tree0['no surfacing'][3] = 'maybe'
    create_plot(tree0)

