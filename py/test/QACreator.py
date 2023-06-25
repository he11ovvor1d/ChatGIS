import pandas as pd

# 定义问答对列表
qa_pairs = []
tablename=("water","poi","street","river","subway","areawater")
ptn=("water","poi","street")
water=("Laoyaba Reservoir","Anjishan Reservoir")
poi=("Jiangsu Liuhe National Geopark","Nanjing Jiangning Tangshan National Geopark","Qixia Mountain National Forest Park","Zijinshan National Forest Park","Nanjing Lukou International Airport","Jiangsu Jiangning Tangshan Fangshan National Geopark","Jiangsu Yangtze River Xinjizhou National Wetland Park")
street=("Chengqiao Street","Donggou Town","Getang Street","Hengliang Subdistrict","Jiangxin Island Street","Jinniuhu Street","Longpao Subdistrict","Ma'an Town","Ma'an Street","Qixia Street","Qilin Street","Tangquan Street","Tangshan Street","Longchi Street","Xingdian Town","Yeshan Street","Changlu Street","Zhuzhen Town","Delivery Village","Dingshan Street","Whitehorse ","Dongba Town","Dongping Town","Cooperstown ","Gucheng Town","Honglan Town","Jingqiao Town","Qiqiao Town","Qiaolin Street","Shiqiu Town","Yaxi Town","Yangjiang Town","Zhetang Town","Binjiang Neighborhood Committee","Chagang Village","Chapeng Village","Fujiatan Neighborhood Committee","Gaotang Village","Hangzhou Village Neighborhood Committee","Airport Road Neighborhood Committee","Jiangjia Village","Nanshan Lake Neighborhood Committee","Shatang'an Neighborhood Committee","Xiyang Neighborhood Committee","New Rural Residents' Committee","Yongyang Town","Chunxi Town","Meishan Street","Hefeng Town","Brick Wall Town")
pdic={water:"water",poi:"poi",street:"street"}
ltn=("river","subway")
river=("Xinqiao River","Banqiao River","Xisuoshu River","Qinhuai New River","Jiexi River","Shiqi River","Tangshui River","Dongshili Changgou","Xinyu River","Jiuxiang River","Huangmu River","Zaohe","Jiangning River","Yongsheng River","Qinhuai River","Chuhe River","Three Rivers","Niu'ergang River","Lishui River","Yuntai Mountain and River","Nanhe River","Grain Transport River","Jiajiang","Macha River","Yuezi River","Chuanzikou River","Xinhuang River","EightHundred Rivers","Siliu River")
subway=("10","1","2","3","S","S8")
ldic={river:"river",subway:"subway"}
atn=("areawater","district")
areawater=("Baijia Lake","Gongtang Reservoir","Zhongshan Reservoir","Convenient Reservoir","Wolong Reservoir","Gucheng Lake","Shijiu Lake","Kowloon Lake","Hewangba Reservoir","Shanhu Reservoir","Jinniushan Reservoir","Xuanwu Lake","Yangtze River")
district=("Luhe District","Qixia District","Xuanwu District","Gulou District","Gaochun District","Lishui District","Jianye District","Qinhuai District","Yuhuatai District","Jiangning District","Pukou District")
adic={areawater:"areawater",district:"district"}
tdic={water:"water",poi:"poi",street:"street",river:"river",subway:"subway",areawater:"areawater"}
tdic1={water:"water",poi:"poi",street:"street",river:"river",subway:"subway",areawater:"areawater"}

question1=("Which district is the _ located in?","Where is the _?","Where can I find the _?","Which area does the _ exist in?","To which district does the _ belong?","Which district does the _ pertain to?","Which district does the _ belong to?","Which district does the _ fall under?","Which district does the _ come under?","Which district does the _ lie in?","Which district is the _ situated in?","In which district is the _ located?","Which district does the _ reside in?","Which district does the _ occupy?","In which district is the _ found?")
question2=("Through which districts does the _ go?","In which districts does the _ run through?","Which districts does the _ cut across?","Which districts does the _ flow across?","Which districts does the _ pass by?","Which districts does the _ go through?","Which districts does the _ traverse?","Which districts does the _ journey through?","In which districts does the _ pass through?","Across which districts does the _ flow?","Which district does the _ pass through?","Which district is the _ flowing through?","Which districts does the _ flow through?","Through which districts does the _ pass?","Which districts does the _ traverse?","Which districts does the _ cross?","Which districts does the _ transit through?")
question3=("Which _ are there in &?","What _ are included in &?","Which _ are located in &?","Which _ are within &?","What _ can be found in &?","What are the _ in &?","What are some _ in &?","Which _ are situated in &?","Which _ are present in &?","What _ are part of &?","What are the _ available in &?","Which _ are present within the borders of &?","What _ can be discovered in &?","Which _ can be found throughout &?","What are the _ that exist in &?","Which _ are situated within the territory of &?","Which _ are located within &'s boundaries?","What are the _ that can be visited in &?")
question4=("Which district border _?","What are the neighboring district of _?","Which district are adjacent to _?","Which district are in close proximity to _?","What district are in contact with _?","Which district share borders with _?","What district are in direct contact with _?","Which district are in immediate vicinity of _?","What are the district that abut _?","Which district are contiguous to _?")
question5=("What is the area of the _?","How large is the _ in terms of area?","What is the total surface area of the _?","What is the size of the _'s expanse?","What is the extent of the _'s area?","How big is the _ in terms of its geographic area?","What is the measurement of the _'s area?","What is the expanse of the _'s territory?","How vast is the area covered by the _?","What is the geographic span of the _?")
question6=("What is the length of the _?","How long is the _?","What is the total distance of the _?","What is the measurement of the length of the _?","How far does the _ stretch?","What is the extent of the _'s length?","What is the distance covered by the _?","What is the overall span of the _?","How vast is the distance of the _?","What is the geographic length of the _?")
question7=("What is the distance from _ to &?","How far is it from _ to &?","What is the measurement of the distance between _ and &?","What is the total span from _ to &?","How long is the distance of the journey from _ to &?","What is the extent of the distance between _ and &?","What is the travel distance from _ to &?","What is the overall length of the route from _ to &?","How vast is the distance covered from _ to &?","What is the geographic separation between _ and &?")
question8=("Where is the nearest & to _?","Where can I find the closest & to _?","What is the location of the & that is nearest to _?","Which & is the nearest to _?","In which place can I find the & that is closest to _?","What is the nearest &'s location in relation to _?","Where can I locate the & that is in closest proximity to _?","What is the closest &'s whereabouts with respect to _?","Which & is situated nearest to _?")
question9=("Where is _ located?","Can you show me the whereabouts of _?","What is the position of _?","Where can I find _?","In which place is _ situated?","Could you please indicate the location of _?","What is the specific spot of _?","Can you provide the exact whereabouts of _?","Where exactly can I locate _?","What is the precise position of _?","Where exactly is _ located?","Can you provide the specific coordinates of _?","What is the precise position of _?","Could you tell me the exact spot where _ can be found?","In which specific place can _ be seen?","Can you guide me to the exact location of _?","Where precisely can _ be pinpointed?","Can you give me the exact whereabouts of _?","What is the designated site of _?","What is the geographic location of _?")
def generate_sentence(template, words1,words2):
    sentence = template
    sentence = sentence.replace('_', words1)
    sentence = sentence.replace('&', words2)
    return sentence
# 创建一个空的DataFrame

#点在哪个行政区
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in pdic:
#     for n in key:
#         for q in question1:
#             string=generate_sentence(q,n)+"#SELECT * FROM district WHERE ST_Intersects(GEOM,(SELECT GEOM FROM {} WHERE NAME = '{}'))".format(pdic[key],n)
#             qa_pairs.append(string)

#线穿过哪个行政区
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in ldic:
#     for n in key:
#         for q in question2:
#             string=generate_sentence(q,n)+"#SELECT * FROM district WHERE ST_Intersects(GEOM,(SELECT GEOM FROM {} WHERE NAME = '{}'))".format(ldic[key],n)
#             qa_pairs.append(string)

#行政区里有哪些
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in district:
#     for n in tablename:
#         for q in question3:
#             string=generate_sentence(q,n,key)+"#SELECT * FROM {} WHERE ST_Intersects(GEOM,(SELECT GEOM FROM district WHERE NAME = '{}'))".format(n,key)
#             qa_pairs.append(string)

#相邻
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in district:
#         for q in question4:
#             string=generate_sentence(q,key,key)+"#SELECT * FROM district WHERE ST_Intersects(GEOM,(SELECT GEOM FROM district WHERE NAME = '{}'))".format(key)
#             qa_pairs.append(string)

#面积
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in adic:
#     for n in key:
#         for q in question5:
#             string=generate_sentence(q,n,n)+"#SELECT ST_Area(GEOM) FROM {} WHERE NAME = '{}'".format(adic[key],n)
#             qa_pairs.append(string)

#长度
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in ldic:
#     for n in key:
#         for q in question6:
#             string=generate_sentence(q,n,n)+"#SELECT ST_Length(GEOM) FROM {} WHERE NAME = '{}'".format(ldic[key],n)
#             qa_pairs.append(string)
# for pair in qa_pairs:
#     question, answer = pair.split('#')
#     df = df.append({'Question':question, 'Answer':answer}, ignore_index=True)
    
#距离
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in tdic:
#     for n in key:
#         for x in tdic1:
#             for m in x:
#                 for q in question7:
#                     string=generate_sentence(q,n,m)+"#SELECT ST_Distance(GEOM,(SELECT GEOM FROM {} WHERE NAME = '{}')) FROM {} WHERE NAME = '{}'".format(tdic[key],n,tdic1[x],m)
#                     qa_pairs.append(string)

#最近
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in tdic:
#         for x in tdic1:
#             for m in x:
#                 for q in question8:
#                     string=generate_sentence(q,m,tdic[key])+"#SELECT * FROM {} ORDER BY ST_Distance(GEOM,(SELECT GEOM FROM {} WHERE NAME = '{}'))LIMIT 1".format(tdic[key],tdic1[x],m)
#                     qa_pairs.append(string)

#位置
# df = pd.DataFrame(columns=['Question', 'Answer'])
# for key in tdic:
#         for m in key:
#             for q in question9:
#                 string=generate_sentence(q,m,m)+"#SELECT * FROM {} WHERE NAME = '{}'".format(tdic[key],m)
#                 qa_pairs.append(string)
# for pair in qa_pairs:
#     question, answer = pair.split('#')
#     df = df.append({'Question':question, 'Answer':answer}, ignore_index=True)

# 将DataFrame写入CSV文件
df1 = pd.read_csv('D:\qa1.csv', sep='#')
# 读取第二个 CSV 文件
df2 = pd.read_csv('D:\qa2.csv', sep='#')
df3 = pd.read_csv('D:\qa3.csv', sep='#')
df4 = pd.read_csv('D:\qa4.csv', sep='#')
df5 = pd.read_csv('D:\qa5.csv', sep='#')
df6 = pd.read_csv('D:\qa6.csv', sep='#')
df7 = pd.read_csv('D:\qa7.csv', sep='#')
df8 = pd.read_csv('D:\qa8.csv', sep='#')
df9 = pd.read_csv('D:\qa9.csv', sep='#')
df10 = pd.read_csv('D:\qa10.csv', sep='#')
# 合并 DataFrame
merged_df = pd.concat([df1, df2,df3,df4,df5,df6,df7,df8,df9,df10])
# 将合并后的 DataFrame 保存到新的 CSV 文件
merged_df.to_csv('D:\merged.csv', sep='#', index=False)
#df.to_csv('D:\qa10.csv', sep='#',index=False)
