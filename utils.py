import json
import spacy

nlp = spacy.load("en_core_web_sm")


def sen2vec(text=''):
    return text.split()


def para2sens(text=''):
    return [str(sen) for sen in nlp(text).sents]


def equal(sen_1='', sen_2=''):
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
    return rs > 0.8


def find(source='', target=''):
    src = para2sens(source)
    tar = para2sens(target)
    rs = []
    for i in range(len(src)):
        for _sen in tar:
            if equal(src[i], _sen):
                rs.append(i)
                break
    return rs


if __name__ == '__main__':
    data = json.load(open('data/data.json', mode='r', encoding='utf-8'))
    out = open('data/out.json', mode='w+')
    outp = dict()
    for ques_id, ques in data.items():
        for ans_id, ans in ques['answers'].items():
            data = dict()
            answer_ext_summ = ans['answer_ext_summ']
            article = ans['article']
            section = ans['section']
            data['section_answer_ext_summ'] = find(section, answer_ext_summ)
            data['article_answer_ext_summ'] = find(article, answer_ext_summ)
            outp[ans_id] = data
            print(ans_id)
    json.dump(outp, out)
    out.close()
