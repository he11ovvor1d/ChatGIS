#!/usr/bin/env python
# -*- coding: utf-8  -*-
#测试训练好的模型

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')# 忽略警告
import sys
import importlib
importlib.reload(sys)
import gensim


if __name__ == '__main__':
    fdir = 'D:\Doc\ChatGIS\\'
    model = gensim.models.Word2Vec.load(fdir + 'wiki.zh.text.model')

    # word = model.wv.most_similar(u"秦淮")
    # for t in word:
    #     print (t[0],t[1])

xzq=["玄武区","秦淮区","建邺区","鼓楼区","浦口区","栖霞区","雨花台区","江宁区","六合区"]
max=0

for a in xzq:
    if model.wv.similarity(a, '秦淮')>max:
        print(a+str(model.wv.similarity(a, '秦淮')))





    # '''
    # word = model.most_similar(positive=[u'皇上',u'国王'],negative=[u'皇后'])
    # for t in word:
    #     print t[0],t[1]
    #
    #
    # print model.doesnt_match(u'太后 妃子 贵人 贵妃 才人'.split())
    # print model.similarity(u'书籍',u'书本')
    # print model.similarity(u'逛街',u'书本')
    # '''


