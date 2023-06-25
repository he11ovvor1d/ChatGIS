# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify
import psycopg2
import json
from flask_cors import CORS
import re
import t5_api
import Openai_api
import BDtranslate
app = Flask(__name__)
CORS(app)
dic={"Line 1":"1号线","Line 2":"2号线","Line 3":"3号线","Line 10":"10号线","Line S1":"S1号线","Line S8":"S8号线","subway":"地铁","street":"行政中心","district":"行政区","areawater":"面状水","water":"水库","Laoyaba Reservoir":"老鸦坝水库","Anjishan Reservoir":"安基山水库","Jiangsu Liuhe National Geopark":"江苏六合国家地质公园","Nanjing Jiangning Tangshan National Geopark":"南京江宁汤山国家地质公园","Qixia Mountain National Forest Park":"栖霞山国家森林公园","Zijinshan National Forest Park":"紫金山国家森林公园","Nanjing Lukou International Airport":"南京禄口国际机场","Jiangsu Jiangning Tangshan Fangshan National Geopark":"江苏江宁汤山方山国家地质公园","Jiangsu Yangtze River Xinjizhou National Wetland Park":"江苏长江新济洲国家湿地公园","Chengqiao Street":"程桥街道","Donggou Town":"东沟镇","Getang Street":"葛塘街道","Hengliang Subdistrict":"横梁街道","Jiangxin Island Street":"江心洲街道","Jinniuhu Street":"金牛湖街道","Longpao Subdistrict":"龙袍街道","Ma'an Town":"马鞍镇","Ma'an Street":"马鞍街道","Qixia Street":"栖霞街道","Qilin Street":"麒麟街道","Tangquan Street":"汤泉街道","Tangshan Street":"汤山街道","Longchi Street":"龙池街道","Xingdian Town":"星甸镇","Yeshan Street":"冶山街道","Changlu Street":"长芦街道","Zhuzhen Town":"竹镇镇","Delivery Village":"送驾村","Dingshan Street":"顶山街道","Whitehorse ":"白马镇","Dongba Town":"东坝镇","Dongping Town":"东屏镇","Cooperstown ":"古柏镇","Gucheng Town":"固城镇","Honglan Town":"洪蓝镇","Jingqiao Town":"晶桥镇","Qiqiao Town":"漆桥镇","Qiaolin Street":"桥林街道","Shiqiu Town":"石湫镇","Yaxi Town":"桠溪镇","Yangjiang Town":"阳江镇","Zhetang Town":"柘塘镇","Binjiang Neighborhood Committee":"滨江居委会","Chagang Village":"茶岗村","Chapeng Village":"茶棚村","Fujiatan Neighborhood Committee":"傅家坛居委会","Gaotang Village":"高塘村","Hangzhou Village Neighborhood Committee":"杭村居委会","Airport Road Neighborhood Committee":"机场路居委会","Jiangjia Village":"姜家村","Nanshan Lake Neighborhood Committee":"南山湖居委会","Shatang'an Neighborhood Committee":"沙塘庵居委会","Xiyang Neighborhood Committee":"西阳居委会","New Rural Residents' Committee":"新农居委会","Yongyang Town":"永阳镇","Chunxi Town":"淳溪镇","Meishan Street":"梅山街道","Hefeng Town":"和凤镇","Brick Wall Town":"砖墙镇","Xinqiao River":"新桥河","Banqiao River":"板桥河","Xisuoshu River":"西索墅河","Qinhuai New River":"秦淮新河","Jiexi River":"解溪河","Shiqi River":"石碛河","Tangshui River":"汤水河","Dongshili Changgou":"东十里长沟","Xinyu River":"新禹河","Jiuxiang River":"九乡河","Huangmu River":"黄木河","Zaohe":"皂河","Jiangning River":"江宁河","Yongsheng River":"永胜河","Qinhuai River":"秦淮河","Chuhe River":"滁河","Three Rivers":"三江河","Niu'ergang River":"牛耳港河","Lishui River":"溧水河","Yuntai Mountain and River":"云台山河","Nanhe River":"南河","Grain Transport River":"运粮河","Jiajiang":"夹江","Macha River":"马汊河","Yuezi River":"岳子河","Chuanzikou River":"划子口河","Xinhuang River":"新篁河","EightHundred Rivers":"八百河","Siliu River":"四柳河","Baijia Lake":"百家湖","Gongtang Reservoir":"公塘湖","Zhongshan Reservoir":"中山湖","Convenient Reservoir":"方便湖","Wolong Reservoir":"卧龙湖","Gucheng Lake":"固城湖","Shijiu Lake":"石臼湖","Kowloon Lake":"九龙湖","Hewangba Reservoir":"河王坝湖","Shanhu Reservoir":"山湖","Jinniushan Reservoir":"金牛山湖","Xuanwu Lake":"玄武湖","Yangtze River":"长江","Luhe District":"六合区","Qixia District":"栖霞区","Xuanwu District":"玄武区","Gulou District":"鼓楼区","Gaochun District":"高淳区","Lishui District":"溧水区","Jianye District":"建邺区","Qinhuai District":"秦淮区","Yuhuatai District":"雨花台区","Jiangning District":"江宁区","Pukou District":"浦口区"}

def replace_keys_with_values(string, dictionary):
    for key, value in dictionary.items():
        string = string.replace(value," "+key+" ")
    return string

def query(sql):
    conn = psycopg2.connect(database="Your database", user="Your user", password="Your password", host="localhost", port="5432")#数据库连接
    cur = conn.cursor()
    cur1 = conn.cursor()
    features = []

    try:
        cur.execute(sql)
        for row in cur.fetchall():
            if(len(row)==1):
                if re.search(r"\ST_Area\b", sql, re.IGNORECASE):
                    return "\"面积是："+str(round(row[0]*10000,2))+"平方公里\""
                else:
                    if re.search(r"\ST_Length\b", sql, re.IGNORECASE):
                        return "\"长度是："+str(round(row[0]*100,2))+"公里\""
                    else:
                        if re.search(r"\ST_Distance\b", sql, re.IGNORECASE):
                            return "\"距离是："+str(round(row[0]*100,2))+"公里\""
            else:
                string=("SELECT ST_AsGeoJSON(ST_GeomFromWKB('\\x{}'))").format(row[1])
                cur1.execute(string)
                feature = {
                "type": "Feature",
                "geometry": json.loads(cur1.fetchall()[0][0]),
                "properties": {"name": dic[row[2]]}}
                features.append(feature)
        gjson = {
        "type": "FeatureCollection",
        "features": features
        }
        conn.commit()
        return jsonify(gjson)
    except psycopg2.Error:
        print("不太明白您的意思，请再试试")
        return "不太明白您的意思，请再试试"
    finally:
        cur1.close()
        cur.close()
        conn.close()


@app.route('/t5', methods=['POST'])
def t5():
    data = request.form['data']
    print(data)
    data1=replace_keys_with_values(data, dic)
    en=BDtranslate.baidu_api(data1)
    sql=t5_api.get_sql(en)
    print(sql)
    return query(sql)

@app.route('/Openai', methods=['POST'])
def Openai():
    data = request.form['data']
    print(data)
    data1=replace_keys_with_values(data, dic)
    en=BDtranslate.baidu_api(data1)
    sql=Openai_api.query(en)
    print(sql)
    return query(sql)

if __name__ == '__main__':
    app.run(port=8000)
