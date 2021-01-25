import json
import spacy
import pandas
from collections import Counter

nlp = spacy.load("en_core_web_sm")


def get_score(array, length_of_seq=2):
    """
    thay thế length_of_seq bằng độ dài các câu liên tiếp ít nhất muốn lấy
    """
    for begin_id in range(len(array) - length_of_seq):
        continuous = True
        for i in range(begin_id, begin_id + length_of_seq):
            if array[i] != array[i + 1] - 1:
                continuous = False
                break
        if continuous:
            return True
    return False


def sen2vec(text=''):
    return text.split()


def para2sens(text=''):
    return [str(sen) for sen in nlp(text).sents]


def equal(sen_1='', sen_2='', threshold=0):
    vec_1 = sen2vec(sen_1.lower())
    vec_2 = sen2vec(sen_2.lower())
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
    return rs >= threshold


def find(source='', target='', src_vec=None, tar_vec=None):
    src = src_vec if src_vec is not None else para2sens(source)
    tar = tar_vec if tar_vec is not None else para2sens(target)
    rs = []
    for i in range(len(src)):
        for _sen in tar:
            if equal(src[i], _sen):
                rs.append(i)
                break
    return rs


def prepare_data(js=None):
    rs = dict()
    for ques_id, ques in js.items():
        rs[ques_id] = dict()
        for ans_id, ans in ques['answers'].items():
            d = dict()
            d['answer_ext_summ'] = para2sens(ans['answer_ext_summ'])
            d['article'] = para2sens(ans['article'])
            d['section'] = para2sens(ans['section'])
            rs[ques_id][ans_id] = d
    return rs


def statistic(data=None, threshold=0, len_of_seq=2):
    article_ratio, article_list = 0, []
    section_ratio, section_list = 0, []
    for ques_id in data:
        for ans_id in data[ques_id]:
            temp = data[ques_id][ans_id]
            article_list.append(get_score(find(src_vec=temp['article'], tar_vec=temp['answer_ext_summ']), len_of_seq))
            section_list.append(get_score(find(src_vec=temp['section'], tar_vec=temp['answer_ext_summ']), len_of_seq))
    article_ratio = Counter(article_list)[True]/ (Counter(article_list)[True]+Counter(article_list)[False])
    section_ratio = Counter(section_list)[True]/ (Counter(section_list)[True]+Counter(section_list)[False])
    return [article_ratio, section_ratio]


def process(data=None):
    data = prepare_data(data)
    outp = dict()
    for tr in range(101):
        threshold = tr / 100
        outp[tr] = statistic(data, threshold)
    rs = pandas.DataFrame(data=outp)
    rs.to_csv('data/out.csv', header=outp.keys())
    return rs


if __name__ == '__main__':
    data = json.load(open('data/data.json', mode='r', encoding='utf-8'))
    process(data)
