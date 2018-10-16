import pymysql
from pandas import DataFrame
import re
import nltk
from nltk.corpus import stopwords
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.sorting import FieldFacet

def get_des_vector():
    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')
    db = pymysql.connect(host="localhost", user="root", passwd="123456", db="project")
    cursor = db.cursor()
    cursor.execute("SELECT name,description,catalog from detail d")
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
    # print(doclist)
    tempdoclist = []
    mydoclist = []

    # r = '[http]{4}\\:\\/\\/([a-zA-Z]|[0-9])*(\\.([a-zA-Z]|[0-9])*)*(\\/([a-zA-Z]|[0-9])*)*\\s?'
    # tags = set(['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'RP', 'RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS'])
    # for index in range(len(doclist)):
    #     text = str(doclist[index])
    #     text = ' '.join([word for word in text.split()])
    #     text = re.sub(r, ' ', text)
    #     words = nltk.word_tokenize(text)
    #     pos_tags = nltk.pos_tag(words)
    #     ret = ' '.join([word for word, pos in pos_tags if pos in tags])
    #     # print(ret)
    #     tempdoclist.append(ret)
    #
    # r1 = '[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、：:;；~@#￥%……&*（）0123456789]+'
    # cachedStopWords = stopwords.words("english")
    # for index in range(len(tempdoclist)):
    #     text = str(tempdoclist[index])
    #     text = ' '.join([word for word in text.split()])
    #     text = re.sub(r1, ' ', text)
    #     text = ' '.join([word for word in text.split() if word not in cachedStopWords])
    #     # print(doclist[index])
    #     # print(text)
    #     # mydoclist.extend(doclist[index])
    #     mydoclist.append(text)

    for i in range(len(doclist)):
        mydoclist.extend(doclist[i])
    print(len(mydoclist))
    print(mydoclist)

    df2 = df[['A']]
    namelist = df2.values
    mynamelist = []
    for i in range(len(namelist)):
        mynamelist.extend(namelist[i])
    print(len(mynamelist))
    print(mynamelist)

    df3 = df[['C']]
    cataloglist = df3.values
    mycataloglist = []
    for i in range(len(cataloglist)):
        mycataloglist.extend(cataloglist[i])
    print(len(mycataloglist))
    print(mycataloglist)

    schema = Schema(name=TEXT(stored=True), description=TEXT(stored=True),
                    catalog=TEXT(stored=True))  # 创建索引结构
    ix = create_in("IndexSearching/index", schema=schema, indexname='indexname')  # path 为索引创建的地址，indexname为索引名称
    writer = ix.writer()
    for i in range(len(mydoclist)):
        writer.add_document(name=str(mynamelist[i]), description=str(mydoclist[i]), catalog=str(mycataloglist[i]))  # 此处为添加的内容
    print("建立完成一个索引")
    writer.commit()
    # 以上为建立索引的过程
    new_list = []
    index = open_dir("IndexSearching/index", indexname='indexname')  # 读取建立好的索引
    with index.searcher() as searcher:
        parser = QueryParser("description", index.schema)#description,搜索域
        myquery = parser.parse("map OR internet OR GPS")
        results = searcher.search(myquery, limit=20)  # limit为搜索结果的限制，默认为10
        for result1 in results:
            print(dict(result1))
            new_list.append(dict(result1))

if __name__ == '__main__':
    get_des_vector()