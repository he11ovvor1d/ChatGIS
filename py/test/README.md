#T5-small-finetuned
##项目结构
* data：所需要的文本
* output：训练出来的模型，无需更改
* generatorSQL.py：生成数据集，即 文本和sql的问答对
* connectDB.py:链接数据库，与数据库进行交互，对数据进行处理
* train2.py：微调模型，更改相应的参数和调整后，生成我们的模型，实现text2sql任务。
* main.py：引用模型，实现输出

##项目思路
* 确定模型
* 数据集【dataset】
* 模型优化

##模型
###t5-small是什么？
* t5-samll是借助huggingface的一个文本to文本的模型
```
https://huggingface.co/t5-small
```
在这个项目中，我们需要通过对t5-small模型微调，实现text2sql的实现。

所以最重要的一步是需要建立我们特有的问答数据集

##数据集的构建

###主要参照generatorSQL.py
* 首先链接数据库，借用百度翻译的API，将我们数据库所有的name名词转成英文，并生成相应的txt文件。
详见data/englishName文件夹。
* 通过之前总结模版，生成我们所需的sql模版，举一例：
![img.png](img.png)
如图所示："ST_Distance","ST_Intersection","ST_Difference"这三个函数的sql是同一个模版，
且已经将我们符合使用这个条件的数据表名称筛选出来。

* 图中的B是functionName:"ST_Distance","ST_Intersection","ST_Difference"，他的参数其实是
两个实体。**接下来进行分析：**


* select gemo from [c] where name = [d] 是一个子查询。作为一个sql模版
```
# 子查询 查询value in tablename
def commonSql(column, tablename, value):
    return "(select " + column + " from " + tablename + " where name= " + "'" + value + "'" + " limit 1)"

```
* 所以可以将该模版简化为 select funname(geom a,geom b)
```
def commonSqlAB(funname,tablename1,value1,tablename2,value2):
    return "select " + funname + "("+ commonSql(column,tablename1,value1) +","+commonSql(column,tablename2,value2)+")"
```
* 建立问答对的主要思路是：用通用的函数问法，只是替换其中的实体。
如：使用ST_Distance函数，一般是问a到b有多远？a到b距离是多少？则通过"distance/how far""是我们的关键词，而a和
b就是我们数据库的实体了。
**"ST_Distance","ST_Intersection","ST_Difference"** 这三个函数的问答对的建立也是如此
```
def generatorAB():
    for tableName1 in tableNames1:
        dic = {}
        valueSimple = pd.read_csv('./data/englishName/' + tableName1 + '.txt', header=None)
        raw_sample = valueSimple.iloc[:, 0]
        for i in raw_sample:
        ****~~~~_**# for循环的作用可以理解为填充a和b两个实体****~~~~_**
            for tableName2 in tableNames1:
                valueSimple2 = pd.read_csv('./data/englishName/' + tableName2 + '.txt', header=None)
                raw_sample2 = valueSimple2.iloc[:, 0]
                for j in raw_sample2:
                **# functionName[3] 是 ST_Distance。**
                    keyValueA = commonSqlAB(functionName[3], tableName1, str(i), tableName2, str(j))
                    key1 = "How far is it from " + str(i) +" to the "+ str(j) +"?"
                    dic[key1] = keyValueA
                    key2 = "What's the distance from "+ str(i) +" to the "+ str(j) +"?"
                    dic[key2] =keyValueA
 **# functionName[4] 是 ST_Intersection。**
                    keyValueB = commonSqlAB(functionName[4], tableName1, str(i), tableName2, str(j))
                    key3 = "What is the common area between " +str(i) +" and "+ str(j) +"?"
                    dic[key3] =keyValueB
                    key4 = "What is the overlap between " + str(i) + " and " + str(j) + "?"
                    dic[key4] = keyValueB
 **# functionName[5] 是 ST_Difference。**
                    keyValueC = commonSqlAB(functionName[5], tableName1, str(i), tableName2, str(j))
                    key5 = "Can you show the area of the " + str(i) + " not overlapped the " + str(j) + "?"
                    dic[key5] = keyValueC
                    key6 = "What part of the " + str(i) + " not covered by " + str(j) + "?"
                    dic[key6] = keyValueC
                df = pd.DataFrame(dic, index=[0]).T
                print(df)
                df.to_csv("absample.csv", sep='#')

```
* 每个函数都根据其特性，生成问答对，并最终将其汇总到一张数据集上。


##模型优化
train2.py

##模型微调基本思路
* 1、选择符合任务的数据集 
* 2、数据预处理：将数据转化为T5可以理解的形式。由于T5是一个基于文本的模型，需要将输入的自然语言查询和输出的SQL查询都转化为文本形式。同时，需要为T5模型制定一个任务前缀，“translate English to SQL:”。
* 3、模型微调：参数调整
* 4、评估和优化：生成是否争取



##尝试
### 返回的sql会出先序列截断
* 1、所以
 `tokenizer.model_max_length = 512`:这行代号设置了tokenizer的最大长度。在NLP中，tokenizer的工作是将输入的文本转换为模型可以理解的格式，通常是一系列的数字。因为模型通常有一定的输入长度限制（对于T5-small模型，这个限制默认是512），这个代码设置了tokenizer在进行这种转换时可以接受的最大长度。 
* 2、在target_encodings中的最大长度为128
### per_device_train_batch_size 批量大小调整
* per_device_train_batch_size=16,比 per_device_train_batch_size=32的效果更好
