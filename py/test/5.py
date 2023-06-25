
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')# 忽略警告
import gensim


if __name__ == '__main__':

    # inp为输入语料, outp1 为输出模型, outp2为原始c版本word2vec的vector格式的模型
    fdir = 'D:\\Doc\\ChatGIS\\model\\'#输入自己的根目录
    inp = fdir + '1.txt'
    outp1 = fdir + 'wiki.zh.text.model'
    outp2 = fdir + 'wiki.zh.text.vector'
    model= gensim.models.Word2Vec.load(fdir + 'wiki.zh.text.model')
    i=0
    s=["江苏六合国家地质公园","六合国家地质公园","国家地质公园","地质公园","公园","地质","国家地质","六合地质公园","六合地质","六合公园","六合"]
    # model.build_vocab(s, update=True)
    # model.train(s,total_examples=model.corpus_count, epochs=model.epochs)
    with open(inp,'r',encoding='utf-8') as f:
        s=f.read()
        model.build_vocab(s, update=True)
        model.train(s,total_examples=model.corpus_count, epochs=model.epochs)
        # for sen in f:
        #     model.build_vocab(sen, update=True)
        #     model.train(sen,total_examples=model.corpus_count, epochs=2)
        #     i+=1
        #     print(i)
    # 保存模型
    model.save(outp1)
    model.wv.save_word2vec_format(outp2, binary=False)



