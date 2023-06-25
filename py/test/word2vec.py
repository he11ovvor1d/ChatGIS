# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')# 忽略警告
import sys
import importlib
importlib.reload(sys)
import gensim
import jieba

fdir = 'model\\'
model = gensim.models.Word2Vec.load(fdir + 'wiki.zh.text.model')
table_value={'江苏六合国家地质公园':'POI',"南京江宁汤山国家地质公园":'POI',"栖霞山国家森林公园":'POI',"紫金山国家森林公园":'POI',"南京禄口国际机场":'POI',"江苏江宁汤山方山国家地质公园":'POI',"江苏长江新济洲国家湿地公园":'POI',"10号线":'地铁',"1号线":'地铁',"2号线":'地铁',"3号线":'地铁',"S1号线":'地铁',"S8号线":'地铁',"老鸦坝水库":'水库',"安基山水库":"水库","新桥河":"河流","板桥河":"河流","西索墅河":"河流","秦淮新河":"河流","解溪河":"河流","石碛河":"河流","汤水河":"河流","东十里长沟":"河流","九乡河":"河流","黄木河":"河流","皂河":"河流","秦淮河":"河流","滁河":"河流","江宁河":"河流","永胜河":"河流","三江河":"河流","牛耳港河":"河流","溧水河":"河流","云台山河":"河流","南河":"河流","运粮河":"河流","夹江":"河流","马汊河":"河流","岳子河":"河流","划子口河":"河流","新禹河":"河流","新篁河":"河流","八百河":"河流","四柳河":"河流","程桥街道":"行政中心","东沟镇":"行政中心","葛塘街道":"行政中心","横梁街道":"行政中心","江心洲街道":"行政中心","金牛湖街道":"行政中心","龙袍街道":"行政中心","马鞍镇":"行政中心","马鞍街道":"行政中心","栖霞街道":"行政中心","麒麟街道":"行政中心","汤泉街道":"行政中心","汤山街道":"行政中心","龙池街道":"行政中心","星甸镇":"行政中心","冶山街道":"行政中心","长芦街道":"行政中心","竹镇镇":"行政中心","送驾村":"行政中心","顶山街道":"行政中心","白马镇":"行政中心","东坝镇":"行政中心","东屏镇":"行政中心","古柏镇":"行政中心","固城镇":"行政中心","洪蓝镇":"行政中心","晶桥镇":"行政中心","漆桥镇":"行政中心","桥林街道":"行政中心","石湫镇":"行政中心","桠溪镇":"行政中心","阳江镇":"行政中心","柘塘镇":"行政中心","滨江居委会":"行政中心","茶岗村":"行政中心","茶棚村":"行政中心","傅家坛居委会":"行政中心","高塘村":"行政中心","杭村居委会":"行政中心","机场路居委会":"行政中心","姜家村":"行政中心","南山湖居委会":"行政中心","沙塘庵居委会":"行政中心","西阳居委会":"行政中心","新农居委会":"行政中心","永阳镇":"行政中心","淳溪镇":"行政中心","梅山街道":"行政中心","和凤镇":"行政中心","砖墙镇":"行政中心","六合区":"行政中心","栖霞区":"行政区","玄武区":"行政区","鼓楼区":"行政区","高淳区":"行政区","溧水区":"行政区","建邺区":"行政区","秦淮区":"行政区","雨花台区":"行政区","江宁区":"行政区","浦口区":"行政区","百家湖":"面状水","公塘水库":"面状水","中山水库":"面状水","方便水库":"面状水","九龙湖":"面状水","卧龙水库":"面状水","固城湖":"面状水","石臼湖":"面状水","河王坝水库":"面状水","山湖水库":"面状水","金牛山水库":"面状水","玄武湖":"面状水","长江":"面状水"}
table_name=["面状水","水库","POI","行政区","行政中心","河流","地铁"]
fun_name={"相交":"st_intersects","包含":"st_intersects","存在":"st_intersects","相邻":"st_touches","穿过":"st_crosses"}
jieba.load_userdict('dic.txt')

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
def process_data(data):
    a,b,c,d=sim(data)
    x="SELECT ST_AsGeoJSON(geom),name FROM {} WHERE {}(geom,(SELECT geom from {} WHERE name = '{}'))".format(a,b,c,d)
    return x
