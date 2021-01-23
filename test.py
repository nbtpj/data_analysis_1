import csv
import json


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


def csv_write(iterable, file):
    for row in iterable:
        for cell in row:
            file.write(str(cell) + ',')
        file.write('\n')
    file.close()


def list2arr(iterable):
    rs = '['
    for i in iterable:
        rs += ' ' + str(i) + ' '
    rs += ']'
    return rs


if __name__ == '__main__':
    data = json.load(open('data/data.json'))
    f = open('data/out.csv', mode='w+', encoding='utf-8')
    writer = csv.writer(f)
    rows = [['ques_id', 'Answer_id', 'section in sum <sen_id>', 'article in sum <sen_id>',
             'sum has continuous sentences in section', 'sum has continuous sentences in article']]
    out = json.load(open('data/out.json'))
    for ques_id, ques in data.items():
        for ans_id, ans in ques['answers'].items():
            _data = out[ans_id]
            print(ans_id)
            print(_data['section_answer_ext_summ'])
            print(_data['article_answer_ext_summ'])
            rows.append([ques_id, ans_id, list2arr(_data['section_answer_ext_summ']),
                         list2arr(_data['article_answer_ext_summ']),
                         get_score(_data['section_answer_ext_summ']),
                         get_score(_data['article_answer_ext_summ'])])
    csv_write(rows, f)
