# -*- coding: utf-8 -*-
import cx_Oracle,warnings,sys,importlib,gensim,jieba,json,atexit
from flask import Flask, request,jsonify
from flask_cors import CORS
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')# 忽略警告
importlib.reload(sys)


app = Flask(__name__)
CORS(app)

#加载Word2Vec模型以及数据字典
fdir = ''
model = gensim.models.Word2Vec.load(fdir + 'wiki.zh.text.model')
#字典示例
table_value={'江苏六合国家地质公园':'POI',"南京江宁汤山国家地质公园":'POI'}
table_name=["面状水","水库","POI","行政区","行政中心","河流","地铁"]
fun_name={"相交":"ANYINTERACT","包含":"ANYINTERACT","存在":"ANYINTERACT","相邻":"TOUCH","穿过":"ANYINTERACT"}
jieba.load_userdict('')

# 连接数据库
conn = cx_Oracle.connect('')
cur = conn.cursor()
#相似度计算
def sim(word):
    max=0
    may=0
    maz=0
    w=x=y=z='没有相关匹配'
    for a in fun_name.keys():
        score1=0
        # print(a+":")
        for b in jieba.cut(word):
            if b in model.wv.key_to_index: 
                score1+=model.wv.similarity(a,b)
                #print(" "+a+","+b+" ",end="")
                #print(model.wv.similarity(a,b))
        if score1>max:
            x=fun_name.get(a)
            max=score1
        #print("Total:",end=" ")
        #print(score1)
    for b in table_value.keys():
        score2=0
        #print(b+":")
        for c in jieba.cut(word):
            if c in model.wv.key_to_index: 
                score2+=model.wv.similarity(c,b)
                #print(" "+b+","+c+" ",end="")
                #print(model.wv.similarity(c,b))
        if score2>may:
            w=b
            y=table_value.get(b)
            may=score2
        #print("Total:",end=" ")
        #print(score2)
    for c in table_name:
        score3=0
        #print(c+":")
        for d in jieba.cut(word):
            if d in model.wv.key_to_index: 
                score3+=model.wv.similarity(c,d)
                #print(" "+c+","+d+" ",end="")
                #print(model.wv.similarity(c,d))
        if score3>maz:
            z=c
            maz=score3
        #print("Total:",end=" ")
        #print(score3)
    return z,x,y,w

#ChatGIS服务程序
@app.route('/process_data', methods=['POST'])

def process_data():
    data = request.form['data']
    print(data)
    a,b,c,d=sim(data)
    x="SELECT SDO_UTIL.TO_GEOJSON(geometry),name FROM {} WHERE SDO_RELATE(geometry,(select geometry from {} where name = '{}'),'MASK={}')='TRUE'".format(a,c,d,b)
    print(x)
    cur.execute(x)
    features = []
    for row in cur.fetchall():
        feature = {
        "type": "Feature",
        "geometry": json.loads(row[0].read()),
        "properties":{"name": row[1]}
       }
        features.append(feature)
    gjson = {
    "type": "FeatureCollection",
    "features": features
    }
    return jsonify(gjson)

if __name__ == '__main__':
    app.run(port=8000)


def exit_handler():
    cur.close()
    conn.close()

atexit.register(exit_handler)



