# -*- coding: utf-8 -*-

# 这是一个使用Python连接数据库并把数据放入DataFrame的方法
# import MySQLdb
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pymysql
from pandas import DataFrame
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

def get_des_vector():
    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')
    db = pymysql.connect(host="localhost", user="root", passwd="ROOT", db="project")
    cursor = db.cursor()
    cursor.execute("SELECT name,description,catalog from detail d")
    # cursor.execute("SELECT name,description,catalog from detail d,recommend r WHERE  d.name = r.host AND (r.r1name in (SELECT name from detail) or r.r2name in (SELECT name from detail) or r.r3name in (SELECT name from detail))")
    # cursor.execute("SELECT name,description,catalog from item i,recommend r WHERE  i.name = r.host AND (r.r1name in (SELECT name from item) or r.r2name in (SELECT name from item) or r.r3name in (SELECT name from item))")
    # cursor.execute("SELECT name,features,catalog,description from detail d,recommend r WHERE d.features <> '' AND d.name = r.host AND (r.r1name in (SELECT name from detail) or r.r2name in (SELECT name from detail) or r.r3name in (SELECT name from detail))")
    # cursor.execute("SELECT name,features,catalog from detail d WHERE d.features <> ''")
    # cursor.execute("SELECT * from traindata")
    data = cursor.fetchall()

    # 这里必须把fetch回来的data转换为list的格式，否则DataFrame会在初始化的时候报错。

    data = list(data)
    data = [list(i) for i in data]

    df = DataFrame(data, columns=["A", "B", "C"])

    # print(df)

    df1 = df[['B']]
    # print(str(df))
    # print(df)
    doclist = df1.values
    print(doclist)
    tempdoclist = []
    mydoclist = []

    r = '[http]{4}\\:\\/\\/([a-zA-Z]|[0-9])*(\\.([a-zA-Z]|[0-9])*)*(\\/([a-zA-Z]|[0-9])*)*\\s?'
    tags = set(['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'RP', 'RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS'])
    for index in range(len(doclist)):
        text = str(doclist[index])
        text = ' '.join([word for word in text.split()])
        text = re.sub(r, ' ', text)
        words = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        ret = ' '.join([word for word, pos in pos_tags if pos in tags])
        # print(ret)
        tempdoclist.append(ret)

    r1 = '[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、：:;；~@#￥%……&*（）0123456789]+'
    cachedStopWords = stopwords.words("english")
    for index in range(len(tempdoclist)):
        text = str(tempdoclist[index])
        text = ' '.join([word for word in text.split()])
        text = re.sub(r1, ' ', text)
        text = ' '.join([word for word in text.split() if word not in cachedStopWords])
        # print(doclist[index])
        # print(text)
        # mydoclist.extend(doclist[index])
        mydoclist.append(text)
    print(len(mydoclist))
    print(mydoclist)

    cursor.execute("SELECT DISTINCT catalog from detail")
    # cursor.execute("SELECT DISTINCT catalog from traindata")
    data1 = cursor.fetchall()
    data1 = list(data1)
    data1 = [list(i) for i in data1]
    df3 = DataFrame(data1, columns=["A"])
    df3 = df3[['A']]
    catalogall = df3.values
    catalog = []
    for i in range(len(catalogall)):
        item = str(catalogall[i]).split('/')
        temp = ''
        if(len(item) > 2):
            temp = item[2]
        else:
            temp = ''
        isin = 0;
        for j in range(len(catalog)):
            if(temp == catalog[j]):
                isin = 1
                break
        if(isin == 0):
            catalog.append(temp)
    # print(catalog)
    print(len(catalog))

    df2 = df[['C']]
    cataloglist = df2.values
    catalogvector = []
    catalognum = []
    for i in range(len(catalog)):
        catalognum.append(0)
    # print(catalognum)
    for i in range(len(cataloglist)):
        item = str(cataloglist[i]).split('/')
        temp = ''
        if (len(item) > 2):
            temp = item[2]
        else:
            temp = ''
        for j in range(len(catalog)):
            if (temp == catalog[j]):
                catalognum[j] = catalognum[j] + 1
                catalogvector.append(j)
                break
    print(catalogvector)


    for i in range(len(catalog)):
        print(str(catalog[i]) + ': ' + str(catalognum[i]))

    catalogother = 0
    for i in range(len(catalogvector)):
        if(catalognum[catalogvector[i]] < 500):
            catalogvector[i] = len(catalognum)
            catalogother = catalogother + 1
    # print(doclist)
    # print(cataloglist)
    print(catalognum)
    print(catalogvector)
    print(len(catalogvector))
    print(catalogother)
    print("null: " + str(catalognum[2]))

    deletetodo = []
    traintodo = []
    mytestlist = []
    testvector = []
    testnum = []
    trainnum = []
    for i in range(len(catalog)):
        testnum.append(0)
        trainnum.append(0)


    for i in range(len(mydoclist)):
        if (catalogvector[i] == 2 or catalogvector[i] == 22 or trainnum[catalogvector[i]] > 700):
            # del mydoclist[i]
            # print("forward: " + str(catalogvector[i]))
            # del catalogvector[i]
            # print("back: " + str(catalogvector[i]))
            # continue
            deletetodo.append(i)
        if(catalogvector[i] != 2 and catalogvector[i] != 22 and (testnum[catalogvector[i]] < catalognum[catalogvector[i]]*0.1)):
            # mytestlist.append(mydoclist[i])
            # del mydoclist[i]
            # testvector.append(catalogvector[i])
            # del catalogvector[i]

            if(catalognum[catalogvector[i]] < 700 or testnum[catalogvector[i]] < 70):
                deletetodo.append(i)
                traintodo.append(i)
                testnum[catalogvector[i]] = testnum[catalogvector[i]] + 1
        if(catalogvector[i] != 22):
            trainnum[catalogvector[i]] = trainnum[catalogvector[i]] + 1

    print("deletetodo: " + str(len(deletetodo)))
    print(deletetodo)
    print("traintodo: " + str(len(traintodo)))
    print(traintodo)

    for i in range(len(traintodo)):
        mytestlist.append(mydoclist[traintodo[i]])
        testvector.append(catalogvector[traintodo[i]])

    # for i in range(len(deletetodo)):
    #     print("error: " + str(deletetodo[i]))
    #     del mydoclist[deletetodo[i]]
    #     del catalogvector[deletetodo[i]]

    # mydoclist = [item for i,item in enumerate(mydoclist) if i not in deletetodo]
    # catalogvector = [item for i,item in enumerate(catalogvector) if i not in deletetodo]

    #增加12维关键词向量
    catalogdeletetodo = []
    catalogdeletetodo.append(2)
    for i in range(len(catalognum)):
        if (catalognum[i] < 500):
            catalogdeletetodo.append(i)
    catalog12 = [item for i, item in enumerate(catalog) if i not in catalogdeletetodo]

    print("catalog12_len: ")
    print(len(catalog12))
    fearures = {}
    for i in range(len(catalog12)):
        fearures.setdefault(catalog12[i],list())

    for i in range(len(catalog12)):
        with open("D:\pyWorkSpace\crawler\\feature\\fact_feature_WFO_" + str(catalog12[i]) + "_150.9.txt",encoding='utf-8') as f:
            lines = f.readlines()
        fearure = fearures.get(catalog12[i])
        print("lines " + str(len(lines)))
        for i in range(len(lines)):
            fearure.append(lines[i].split('\n')[0])

    keylist = {}
    for i in range(len(doclist)):
        keylist.setdefault(i, list())
    stemmer = SnowballStemmer("english")
    for i in range(len(doclist)):
        # print(stemmer.stem(catalog[catalogvector[i]]) + ": " + str(i))
        # if(i == 1):
        #     print(doclist[i][0])
        for j in range(len(catalog12)):
            featuretemp = fearures.get(catalog12[j])
            featurevalue = 0
            for m in range(len(featuretemp)):
                # print(stemmer.stem(featuretemp[m]))
                # print(doclist[i][0])
                if (stemmer.stem(featuretemp[m]) in doclist[i][0]):
                    # print(stemmer.stem(featuretemp[m]))
                    featurevalue =  featurevalue + 1
            key = keylist.get(i)
            # print("value " + str(featurevalue))
            key.append(featurevalue)
            # keylist.__setattr__(str(i),key)

    print("keylenth: " + str(len(keylist)))
    print(keylist.get(3))

    print(len(mydoclist))
    print(len(catalogvector))
    print(len(mytestlist))
    print(len(testvector))



    tfidf_vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(mydoclist)
    # doc = ['This is a map internet web service based on a huge raster maps or satellite images for tracking and monitoring the mobile objects (cars etc) using GPS.']
    # doc = []
    # doc.append(des)
    # newvector = tfidf_vectorizer.transform(doc)
    # return  newvector.todense().tolist()[0]

# print(tfidf_matrix)
# tfidf_matrix.todense()

    f = open("D:\pyWorkSpace\crawler\data\pos_train.txt","r+")

    for i in range(len(mydoclist)):
        if i not in deletetodo:
            vector = tfidf_matrix[i].todense().tolist()[0]
            line = str(catalogvector[i]) + ' '
            for j in range(len(vector)):
                if (vector[j] != 0):
                    line = line + '%s' % (j) + ':' + '%s' % (vector[j]) + ' '
            # if(catalogvector[i] == 2 or catalogvector[i] == 5 or catalogvector[i] == 6):
            #     f.write(line + '\n')
            # if(catalogvector[i] == 4 or catalogvector == 7 or catalogvector[i] == 8 or catalogvector[i] == 10 or catalogvector[i] == 11
            # or catalogvector[i] == 12 or catalogvector[i] ==16):
            #     f.write(line + '\n')
            #     f.write(line + '\n')
            # if(i in keylist.keys()):


            # key = keylist.get(i)
            # print(key)
            # for i in range(len(key)):
            #     line = line + '%s' % (len(vector) + i) + ':' + '%s' % (key[i]) + ' '
            f.write(line + '\n')

    f.close()

    f = open("D:\pyWorkSpace\crawler\data\pos_test.txt","r+")

    for i in range(len(mydoclist)):
        if i in traintodo:
            vector = tfidf_matrix[i].todense().tolist()[0]
            line = str(catalogvector[i]) + ' '
            for j in range(len(vector)):
                if (vector[j] != 0):
                    line = line + '%s' % (j) + ':' + '%s' % (vector[j]) + ' '
            # if(catalogvector[i] == 2 or catalogvector[i] == 5 or catalogvector[i] == 6):
            #     f.write(line + '\n')
            # if(catalogvector[i] == 4 or catalogvector == 7 or catalogvector[i] == 8 or catalogvector[i] == 10 or catalogvector[i] == 11
            # or catalogvector[i] == 12 or catalogvector[i] ==16):
            #     f.write(line + '\n')
            #     f.write(line + '\n')
            # if (i in keylist):


            # key = keylist.get(i)
            # for i in range(len(key)):
            #     line = line + '%s' % (len(vector) + i) + ':' + '%s' % (key[i]) + ' '
            f.write(line + '\n')

    f.close()

if __name__ == '__main__':
    get_des_vector()

# with open('D:\pyWorkSpace\crawler\data\dtrainData.txt.out') as f:
#     lines = f.readlines() # 读取文本中所有内容，并保存在一个列表中，列表中每一个元素对应一行数据
#
# label = []
# correct = 0;
#
#
# class data:
#     def __init__(self,label,probability):
#         self.label = label
#         self.probability = probability
#
#     def __repr__(self):
#         return repr((self.label, self.probability))
#
# print("line: " + str(len(lines)))
# for i in range(len(lines)):
#     vector = lines[i].split(' ')
#     if(i == 0):
#         for j in range(len(vector)):
#             if(j != 0):
#                 if(j == 12):
#                     vector[j] = vector[j].split("\n")[0]
#                 label.append(vector[j])
#         print(label)
#     else:
#         del vector[0]
#         dataList = []
#         for m in range(len(vector)):
#             dataList.append(data(label[m],vector[m]))
#             # print("label: " + label[m] + " vector: " + vector[m])
#             # print("label: " + dataList[m].label + " vector: " + dataList[m].probability)
#         dataList = sorted(dataList,key=lambda data:data.probability,reverse=True)
#         for n in range(len(vector)):
#             print("label: " + dataList[n].label + " vector: " + dataList[n].probability)
#         for j in range(6):
#             print('%s' % (i) + " v1: " + str(dataList[j].label) + " v2: " + str(catalogvector[i]))
#             if(i != len(lines) - 1):
#                 print((int)(dataList[j].label) == testvector[i])
#                 if((int)(dataList[j].label) == testvector[i]):
#                     print("================")
#                     correct = correct + 1
#                     break
#
# print(correct)
# accuracy = (float)(correct/len(mytestlist))
# print(accuracy)



