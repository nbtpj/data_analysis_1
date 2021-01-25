from utils import *
import math

def expect(iterable):
    return sum([i/len(iterable) for i in iterable])

def standard_deviation(iterable):
    e = expect(iterable)
    n = len(iterable)
    return e, math.sqrt(sum([(i/n - e/n)**2 for i in iterable]))

def get_num_words(src):
    return sum([len(i) for i in src])

def get_ratio(src, tar):
    return len(tar)/len(src)

def process_ratio(js=None, base = 'sentence'):
    data = prepare_data(js)
    rs_section, rs_article = [], []
    for ques_id, ques in data.items():
        for ans_id, ans in ques.items():
            section = ans['section']
            sum = ans['answer_ext_summ']
            article = ans['article']
            if base.lower() == 'sentence':
                rs_article.append(get_ratio(article, sum))
                rs_section.append(get_ratio(section, sum))
            else:
                rs_article.append(get_num_words(sum)/get_num_words(article))
                rs_section.append(get_num_words(sum)/get_num_words(section))
    return rs_article, rs_section

def process_fix_len(js=None, base = 'sentence'):
    data = prepare_data(js)
    rs = []
    for ques_id, ques in data.items():
        for ans_id, ans in ques.items():
            sum = ans['answer_ext_summ']
            if base.lower() == 'sentence':
                rs.append(len(sum))
            else:
                rs.append(get_num_words(sum))
    return rs


if __name__ == '__main__':
    print(' tỉ lệ nén (theo câu)')
    rs_article, rs_section = process_ratio()
    e, d = standard_deviation(rs_article)
    print('nguồn nén = article : kì vọng (trung bình) = {} , lệch chuẩn = {}'.format(str(e), str(d)))
    e, d = standard_deviation(rs_section)
    print('nguồn nén = section : kì vọng (trung bình) = {} , lệch chuẩn = {}'.format(str(e), str(d)))
    print('__________________________________')
    print(' tỉ lệ nén (theo từ)')
    rs_article, rs_section = process_ratio(base='word')
    e, d = standard_deviation(rs_article)
    print('nguồn nén = article : kì vọng (trung bình) = {} , lệch chuẩn = {}'.format(str(e), str(d)))
    e, d = standard_deviation(rs_section)
    print('nguồn nén = section : kì vọng (trung bình) = {} , lệch chuẩn = {}'.format(str(e), str(d)))
    print('__________________________________')
    print(' số câu trung bình trong 1 đoạn tóm tắt')
    rs = process_fix_len()
    e, d = standard_deviation(rs)
    print('kì vọng (trung bình) = {} , lệch chuẩn = {}'.format(str(e), str(d)))
    print('__________________________________')
    print(' số từ trung bình trong 1 đoạn tóm tắt')
    rs = process_fix_len(base='word')
    e, d = standard_deviation(rs)
    print('kì vọng (trung bình) = {} , lệch chuẩn = {}'.format(str(e), str(d)))