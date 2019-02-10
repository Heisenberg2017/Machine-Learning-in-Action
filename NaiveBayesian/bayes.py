# -*- coding:utf-8 -*-

'''
朴素贝叶斯分类器
    * 使用朴素贝叶斯进行文本分类
    * 使用朴素贝叶斯过滤垃圾邮件
    * 使用朴素贝叶斯进行交叉验证
'''

import random
import numpy as np
import feedparser


def load_data_set():
    posting_list = [['my', 'dog', 'has', 'flea', 'problem', 'help', 'please'],
                    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park',
                     'stupid'],
                    ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                    ['stop', 'posting', 'stupid', 'worthless', 'garbage', ],
                    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop',
                     'him'],
                    ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]
    return posting_list, class_vec


def create_vocab_list(data_set):
    vocab_set = set([])
    for document in data_set:
        vocab_set = vocab_set | set(document)
    return list(vocab_set)


def set_of_words2vec(vocab_list, input_set):
    return_vec = [0] * len(vocab_list)
    for word in input_set:
        if word in vocab_list:
            return_vec[vocab_list.index(word)] = 1
        else:
            print 'the word: %s if not in my Vocabulary!' % word
    return return_vec


def train_nb0(train_matrix, train_category):
    num_train_docs = len(train_matrix)
    num_words = len(train_matrix[0])
    pa_busive = sum(train_category) / float(num_train_docs)
    # 由于要计算p(w0|1)p(w1|1)p(w2|1)
    # 1.为了避免其中一个值为0导致乘积为0 使 zeros -> ones, *_denom = 0.0 -> *_denom = 2.0
    p0_num = np.ones(num_words)
    p1_num = np.ones(num_words)
    p0_denom = 2.0
    p1_denom = 2.0
    print train_matrix
    for i in range(num_train_docs):
        if train_category[i] == 1:
            p1_num += train_matrix[i]
            p1_denom += sum(train_matrix[i])
        else:
            p0_num += train_matrix[i]
            p0_denom += sum(train_matrix[i])
    # 2.下溢出问题 对乘积取自然对数
    p1_vect = np.log(p1_num / p1_denom)
    p0_vect = np.log(p0_num / p0_denom)
    return p0_vect, p1_vect, pa_busive


def classify_NB(vec2classify, p0_vec, p1_vec, p_class1):
    p1 = sum(vec2classify * p1_vec) + np.log(p_class1)
    p0 = sum(vec2classify * p0_vec) + np.log(1.0 - p_class1)
    if p1 > p0:
        return 1
    else:
        return 0


def testing_NB():
    list_o_posts, list_classes = load_data_set()
    my_vocab_list = create_vocab_list(list_o_posts)
    train_mat = []
    for postin_doc in list_o_posts:
        train_mat.append(set_of_words2vec(my_vocab_list, postin_doc))
    p0_v, p1_v, p_ab = train_nb0(np.array(train_mat), np.array(list_classes))
    test_entry = ['love', 'my', 'dalmation']
    this_doc = np.array(set_of_words2vec(my_vocab_list, test_entry))
    print test_entry, 'classified as: ', classify_NB(this_doc, p0_v, p1_v, p_ab)
    test_entry = ['stupid', 'dalmation']
    this_doc = np.array(set_of_words2vec(my_vocab_list, test_entry))
    print test_entry, 'classified as: ', classify_NB(this_doc, p0_v, p1_v, p_ab)


def bag_of_words2vec_MN(vocab_list, input_set):
    return_vec = [0] * len(vocab_list)
    for word in input_set:
        if word in vocab_list:
            return_vec[vocab_list.index(word)] += 1
    return return_vec


def text_parse(big_string):
    import re
    list_of_tokens = re.split(r'\W*', big_string)
    return [tok.lower() for tok in list_of_tokens if len(tok) > 2]


def spam_test():
    doc_list = []
    class_list = []
    full_text = []
    for i in range(1, 26):
        with open('email/spam/%d.txt' % i) as fr:
            word_list = text_parse(fr.read())
            doc_list.append(word_list)
            full_text.extend(word_list)
            class_list.append(1)
        with open('email/ham/%d.txt' % i) as fr:
            word_list = text_parse(fr.read())
            doc_list.append(word_list)
            full_text.extend(word_list)
            class_list.append(0)
    vocab_list = create_vocab_list(doc_list)
    training_set = range(50)
    test_set = []
    for i in range(10):
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])
    train_mat = []
    train_classes = []
    for doc_index in training_set:
        train_mat.append(set_of_words2vec(vocab_list, doc_list[doc_index]))
        train_classes.append(class_list[doc_index])
    p0_v, p1_v, p_spam = train_nb0(np.array(train_mat), np.array(train_classes))
    error_count = 0
    for doc_index in test_set:
        word_vector = set_of_words2vec(vocab_list, doc_list[doc_index])
        if classify_NB(np.array(word_vector), p0_v, p1_v, p_spam
                       ) != class_list[doc_index]:
            error_count += 1
    print 'the error rate is: ', float(error_count) / len(test_set)


def calc_most_freq(vocab_list, full_text):
    import operator
    freq_dict = {}
    for token in vocab_list:
        freq_dict[token] = full_text.count(token)
    sorted_freq = sorted(freq_dict.iteritems(), key=operator.itemgetter(1),
                         reverse=True)
    return sorted_freq[:20]


def local_words(feed1, feed0):
    import feedparser
    doc_list = []
    class_list = []
    full_text = []
    min_len = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(min_len):
        word_list = text_parse(feed1['entries'][i]['summary'])
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(1)
        word_list = text_parse(feed0['entries'][i]['summary'])
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(0)
    vocab_list = create_vocab_list(doc_list)
    top30_words = calc_most_freq(vocab_list, full_text)
    for pair_w in top30_words:
        if pair_w[0] in vocab_list:
            vocab_list.remove(pair_w[0])
    training_set = range(2 * min_len)
    test_set = []
    for i in range(10):
        rand_index = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[rand_index])
        del(training_set[rand_index])
    train_mat = []
    train_classes = []
    for doc_index in training_set:
        train_mat.append(bag_of_words2vec_MN(vocab_list, doc_list[doc_index]))
        train_classes.append(class_list[doc_index])
        p0_v, p1_v, p_spam = train_nb0(np.array(train_mat), np.array(train_classes))
        error_count = 0
        for doc_index in test_set:
            word_vector = bag_of_words2vec_MN(vocab_list, doc_list[doc_index])
            if classify_NB(np.array(word_vector), p0_v, p1_v, p_spam) != class_list[doc_index]:
                error_count += 1
        print 'the error rate is: ', float(error_count) / len(test_set)
        return vocab_list, p0_v, p1_v


def get_top_words(rss0, rss1):
    import operator
    vocab_list, p0_v, p1_v = local_words(rss0, rss1)
    top_rss0 = []
    top_rss1 = []
    for i in range(len(p0_v)):
        if p0_v[i] > -6.0:
            top_rss0.append((vocab_list[i], p0_v[i]))
        if p1_v[i] > -6.0:
            top_rss1.append((vocab_list[i], p1_v[i]))
    sorted_rss0 = sorted(top_rss0, key=lambda pair: pair[1], reverse=True)
    print '**rss0**rss0**rss0**rss0**rss0**rss0**'
    for item in sorted_rss0[:5]:
        print item
    sorted_rss1 = sorted(top_rss1, key=lambda pair: pair[1], reverse=True)
    print '**rss1**rss1**rss1**rss1**rss1**rss1**'
    for item in sorted_rss1[:5]:
        print item




if __name__ == '__main__':
    # list_o_posts, list_classes = load_data_set()
    # my_vocab_list = create_vocab_list(list_o_posts)
    # print my_vocab_list
    # print set_of_words2vec(my_vocab_list, list_o_posts[0])
    # print set_of_words2vec(my_vocab_list, list_o_posts[3])
    # train_mat = []
    # for postin_doc in list_o_posts:
    #     train_mat.append(set_of_words2vec(my_vocab_list, postin_doc))
    # p0_v, p1_v, p_ab = train_nb0(train_mat, list_classes)
    # print p0_v
    # print p1_v
    # print p_ab
    # testing_NB()
    # spam_test()
    rss0 = feedparser.parse('https://sports.yahoo.com/nba/rss.xml')
    rss1 = feedparser.parse('http://www.nasa.gov/rss/dyn/image_of_the_day.rss')
    vocab_list, p_rss0, p_rss1 = local_words(rss0, rss1)
    vocab_list, p_rss0, p_rss1 = local_words(rss0, rss1)
    vocab_list, p_rss0, p_rss1 = local_words(rss0, rss1)
    vocab_list, p_rss0, p_rss1 = local_words(rss0, rss1)
    print '**top**top**top**top**top**top**'
    get_top_words(rss0, rss1)