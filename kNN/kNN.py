import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt
import os


def create_data_set():
    data_set = np.array([
        [1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return data_set, labels

def classify0(in_x, data_set, labels, k):
    data_set_size = data_set.shape[0]
    diff_mat = np.tile(in_x, (data_set_size, 1)) - data_set
    sq_diff_mat = diff_mat**2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances**0.5
    sorted_dist_indicies = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_i_label = labels[sorted_dist_indicies[i]]
        class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1
        sorted_class_count = sorted(class_count.iteritems(),
            key=operator.itemgetter(1), reverse=True)
    return sorted_class_count

def file2matrix(filename):
    fr = open(filename)
    array_on_lines = fr.readlines()
    number_of_lines = len(array_on_lines)
    return_mat = np.zeros((number_of_lines, 3))
    class_label_vector = []
    index = 0
    for line in array_on_lines:
        line = line.strip()
        list_from_line = line.split('\t')
        return_mat[index, :] = list_from_line[0:3]
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return return_mat, class_label_vector

def auto_norm(data_set):
    min_vals = data_set.min(0)
    max_vals = data_set.max(0)
    ranges = max_vals - min_vals
    norm_data_set = np.zeros(np.shape(data_set))
    m = data_set.shape[0]
    norm_data_set = data_set - np.tile(min_vals, (m, 1))
    norm_data_set = norm_data_set / np.tile(ranges, (m ,1))
    return norm_data_set, ranges, min_vals

def dating_class_test():
    ho_ratio = 0.10
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m * ho_ratio)
    error_count = 0.0
    for i in range(num_test_vecs):
        classifier_result = classify0(
            norm_mat[i,:], 
            norm_mat[num_test_vecs: m, :],
            dating_labels[num_test_vecs: m], 5)
        if (classifier_result[0][0] != dating_labels[i]) : error_count += 1.0
    print 'the total error rate is: %f' % (error_count/ float(num_test_vecs))

def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tats = float(raw_input('percentage of time spent playing video games?'))
    ff_miles = float(raw_input('frequent flier miles earned per year?'))
    ice_cream = float(raw_input('liters of ice cream consume per year?'))
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    in_arr = np.array([ff_miles, percent_tats, ice_cream])
    classifier_result = classify0(
        (in_arr - min_vals)/ ranges, norm_mat, dating_labels, 3)
    print 'You will probably like this person :', result_list[classifier_result[0][0] - 1]


def img2vector(filename):
    return_vect = np.zeros((1, 1024))
    fr = open(filename)
    for i in range(32):

        line_str =  fr.readline()
        for j in range(32):
            return_vect[0, 32 * i+j] = int(line_str[j])
    return return_vect

def hand_writing_class_test():
    hw_labels = []
    training_file_list = os.listdir('digits/testDigits')
    m = len(training_file_list)
    training_mat = np.zeros((m, 1024))
    for i in range(m):
        file_name_str = training_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_number_str = int(file_str.split('_')[0])
        hw_labels.append(class_number_str)
        training_mat[i: 
        ] = img2vector('digits/trainingDigits/%s' % file_name_str)
    test_file_list = os.listdir('digits/testDigits')
    error_count = 0.0
    m_test = len(test_file_list)
    for i in range(m_test):
        file_name_str = test_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_num_str = int(file_str.split('_')[0])
        ventor_under_test = img2vector('digits/testDigits/%s' % file_name_str)
        classifier_result = classify0(ventor_under_test, training_mat, hw_labels, 3)
        print 'the classifier came back with: %d the real answer is: %d' % (classifier_result[0][0], class_num_str)
        if (classifier_result[0][0] != class_num_str): error_count += 1.0
    print '\nthe total number of errors is %d' % error_count
    print '\nthe total error rate is: %f' % (error_count/float(m_test))





if __name__ == '__main__':
    # kNN demo1
    # g, l = create_data_set()
    # print classify0([0, 0], g, l, 3)
    # kNN demo2
    # dating_data_mat, labels = file2matrix('datingTestSet2.txt')
    # print dating_data_mat, labels
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(dating_data_mat[:, 1], dating_data_mat[:, 2],
    #     15.0 * np.array(labels), 15.0 * np.array(labels))
    # plt.show()
    # kNN demo3
    # ax.scatter(dating_data_mat[:, 0], dating_data_mat[:, 1],
    #     15.0 * np.array(labels), 15.0 * np.ar''ray(labels))
    # plt.show()  
    # norm process
    # norm_data_set, ranges, min_vals = auto_norm(dating_data_mat)
    # ax.scatter(norm_data_set[:, 0], norm_data_set[:, 1],
    #     15.0 * np.array(labels), 15.0 * np.array(labels))
    # plt.show()
    # dating_class_test()
    # classify_person()
    # test_vector = img2vector('digits/testDigits/0_13.txt')
    # print test_vector[0, 0:31]
    hand_writing_class_test()