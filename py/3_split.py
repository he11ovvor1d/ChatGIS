import jieba
import re

# 读取文件
with open('C:\\Users\\10675\\Desktop\\outputnews.txt', 'r', encoding='utf-8') as f1, open('C:\\Users\\10675\\Desktop\\split_news.txt', 'w',encoding='utf-8') as f2:
    text = f1.read()
    # 分句
    sentences = re.split('[。！？]', text)
# 去除标点
    punctuation = r'[^\w\s]+'
    for s in sentences:
        x = re.sub(punctuation, '', s)
        w=jieba.cut(x)
        for ww in w:
            f2.write(ww+' ')
        f2.write('\n')
    f1.close()
    f2.close()

