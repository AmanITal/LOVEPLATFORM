import time
import jieba
import os


def get_emotion(score):
    emotion_archive = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    if score <= -3.9:
        return emotion_archive[0]
    elif -3.9 < score <= -2.5:
        return emotion_archive[1]
    elif -2.5 < score <= -1:
        return emotion_archive[2]
    elif -1 < score <= 0:
        return emotion_archive[3]
    elif 0 < score <= 1:
        return emotion_archive[4]
    elif 1 < score <=2.5:
        return emotion_archive[5]
    elif 2.5 < score <= 3.9:
        return emotion_archive[6]
    else:
        return emotion_archive[7]


def compute_model(content):
    emotion_dic =   {}
    senList     =   str()
    filename    =   os.path.abspath(os.path.dirname(__file__)) + '\\static\\BosonNLP\\BosonNLP_sentiment_score.txt'
    with open(filename, 'rb') as files:
        while 1:
            try:
                senList                 =   (files.readline()).decode('utf-8')
                # print(senList)
                senList                 =   senList[:-1]
                senList                 =   senList.split(' ')
                emotion_dic[senList[0]] =   senList[1]
            except IndexError:
                break
    seg_list        =   jieba.cut(content, cut_all=True)
    string          =   "/".join(seg_list)
    string_list     =   string.split('/')
    emotion_index   =     0
    time.sleep(1)
    ''''
        -5分为极端消极评论
        5分为过于积极评论
    '''
    for _ in range(len(string_list)):
        if string_list[_-1] in emotion_dic:
            emotion_index += float(emotion_dic[string_list[_-1]])
    return emotion_index

if __name__ == '__main__':
    content = '这个数字有点高了，我也有些为难'
    print(compute_model(content))