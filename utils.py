import json
import spacy
import pandas
import os
from collections import Counter
from ratio import *
from rouge import Rouge

# import matplotlib.pyplot as plt
nlp = spacy.load("en_core_web_sm")


def get_score(array, length_of_seq=2):
    """
    thay thế length_of_seq bằng độ dài các câu liên tiếp ít nhất muốn lấy
    """
    for begin_id in range(len(array) - length_of_seq):
        continuous = True
        for i in range(begin_id, begin_id + length_of_seq):
            if int(array[i]) != int(array[i + 1]) - 1:
                continuous = False
                break
        if continuous:
            return True
    return False


def get_seq_len_list(array):
    rs = []
    curr = None
    len = None
    for i in array:
        n = int(i)
        if curr is None:
            curr = n
            len = 1
        else:
            if n != curr + 1:
                rs.append(len)
                len = 1
                curr = n
            else:
                curr = n
                len += 1
    if len is not None:
        rs.append(len)
    return rs


def sen2vec(text=''):
    return text.split()


def para2sens(text=''):
    return [str(sen) for sen in nlp(text).sents]


def para2dict(text=''):
    sens = para2sens(text)
    rs = dict()
    for sen_id in range(len(sens)):
        rs[sen_id] = sen2vec(sens[sen_id])
    return rs


def equal(sen_1='', sen_2='', threshold=0.0, v_1=None, v_2=None, similarity=False):
    vec_1 = v_1 if v_1 is not None else sen2vec(sen_1.lower())
    vec_2 = v_2 if v_2 is not None else sen2vec(sen_2.lower())
    if len(vec_1) * len(vec_2) == 0:
        return False
    rs_1, rs_2 = [False for _ in vec_1], [False for _ in vec_2]
    n_1 = n_2 = 0
    for i in range(len(vec_1)):
        for j in range(len(vec_2)):
            if vec_1[i] == vec_2[j] and not rs_2[j]:
                rs_1[i] = rs_2[j] = True
                n_1 += 1
                n_2 += 1
    rs = (n_1 / len(vec_1) + n_2 / len(vec_2)) / 2
    if similarity:
        return rs
    return rs >= threshold


def find(source='', target='', src_dict=None, tar_dict=None, threshold=0.0):
    src = src_dict if src_dict is not None else para2dict(source)
    tar = tar_dict if tar_dict is not None else para2dict(target)
    rs = []
    for i_1, s_1 in src.items():
        for i_2, s_2 in tar.items():
            if equal(v_1=s_1, v_2=s_2, threshold=threshold):
                rs.append(i_1)
                break
    return rs


def prepare_data(js=None):
    if os.path.exists('data/input.json'):
        try:
            rs = json.load(open('data/input.json'))
            return rs
        except:
            pass
    rs = dict()
    for ques_id, ques in js.items():
        rs[ques_id] = dict()
        for ans_id, ans in ques['answers'].items():
            d = dict()
            d['answer_ext_summ'] = para2dict(ans['answer_ext_summ'])
            d['article'] = para2dict(ans['article'])
            d['section'] = para2dict(ans['section'])
            rs[ques_id][ans_id] = d
    json.dump(rs, open('data/input.json', 'w+'))
    return rs


def statistic(data=None, threshold=0.0, len_of_seq=4):
    article_ratio, article_list = 0, []
    section_ratio, section_list = 0, []
    for ques_id in data:
        for ans_id in data[ques_id]:
            temp = data[ques_id][ans_id]
            article_list.append(
                get_score(find(src_dict=temp['article'], tar_dict=temp['answer_ext_summ'], threshold=threshold),
                          len_of_seq))
            section_list.append(
                get_score(find(src_dict=temp['section'], tar_dict=temp['answer_ext_summ'], threshold=threshold),
                          len_of_seq))
    article_ratio = Counter(article_list)[True] / (len(article_list))
    section_ratio = Counter(section_list)[True] / (len(section_list))
    return [article_ratio, section_ratio]


def statistic_len_list(data=None, threshold=0.0):
    article_list = []
    section_list = []
    for ques_id in data:
        for ans_id in data[ques_id]:
            temp = data[ques_id][ans_id]
            article_list.extend(
                get_seq_len_list(find(src_dict=temp['article'], tar_dict=temp['answer_ext_summ'], threshold=threshold)))
            section_list.extend(
                get_seq_len_list(find(src_dict=temp['section'], tar_dict=temp['answer_ext_summ'], threshold=threshold)))
    e_ar, d_ar = standard_deviation(article_list)
    e_sec, d_sec = standard_deviation(section_list)
    return e_ar, d_ar, e_sec, d_sec


def process_ratio_of_seq(data=None):
    data = prepare_data(data)
    outp = dict()
    article_sc = []
    section_sc = []
    thres = []
    for tr in range(101):
        threshold = tr / 100
        thres.append(threshold)
        outp[tr] = statistic(data, threshold)
        article_sc.append(outp[tr][0])
        section_sc.append(outp[tr][1])
    rs = pandas.DataFrame(data=outp)
    rs.to_csv('data/out.csv', header=outp.keys())
    json.dump(outp, open('data/output.json', 'w+'))
    return rs, article_sc, section_sc, thres


def process_aver_len_of_seq(data=None):
    data = prepare_data(data)
    outp = dict()
    article_sc = []
    section_sc = []
    thres = []
    outp['entities'] = ['expect_article', 'standard_deviation_article', 'expect_section', 'standard_deviation_section']
    for tr in range(101):
        threshold = tr / 100
        thres.append(threshold)
        e_ar, d_ar, e_sec, d_sec = statistic_len_list(data, threshold)
        outp[tr] = [e_ar, d_ar, e_sec, d_sec]
    json.dump(outp, open('data/output_v2.json', 'w+'))
    rs = pandas.DataFrame(data=outp)
    rs.to_csv('data/out_v2.csv', header=outp.keys())

    return rs, article_sc, section_sc, thres


if __name__ == '__main__':
    data = json.load(open('data/data.json', mode='r', encoding='utf-8'))
    rs, article, section, label = process_aver_len_of_seq(data)
    # fig, ax = plt.subplots()
    # ax.plot(label, article)
    # ax.plot(label, section)
    # ax.set(xlabel='threshold of sim function', ylabel='ratio',
    #        title='data analysis')
    # ax.grid()
    # plt.show()
