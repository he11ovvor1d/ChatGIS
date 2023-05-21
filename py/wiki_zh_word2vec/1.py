# -*- coding: utf-8 -*-
from gensim.corpora import WikiCorpus
import jieba


def my_function():
    space = ' '
    i = 0
    l = []
    zhwiki_name = 'F:\zhwiki-latest-pages-articles.xml.bz2'#输入zhwiki-latest-pages-articles.xml.bz2的路径
    f = open('zhiwiki.txt', 'w', encoding='utf-8')#输入输出文件的路径
    wiki = WikiCorpus(zhwiki_name, dictionary={})  # 从xml文件中读出训练语料
    for text in wiki.get_texts():
        for temp_sentence in text:
      
            seg_list = list(jieba.cut(temp_sentence))  # 分词
            for temp_term in seg_list:
                l.append(temp_term)
        f.write(space.join(l) + '\n')
        l = []
        i = i + 1

        if (i % 200 == 0):
            print('Saved ' + str(i) + ' articles')
    f.close()


if __name__ == '__main__':
    my_function()