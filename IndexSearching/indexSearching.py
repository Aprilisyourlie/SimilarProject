from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *

def get_indexSearching_result(request):
    new_list = []
    name_list = []
    catalog_list = []
    description_list = []
    index = open_dir("IndexSearching/index", indexname='indexname')  # 读取建立好的索引
    requestSplit = []
    requestNew = ''
    requestSplit = request.split(" ")
    print(requestSplit)
    for i in range(len(requestSplit)):
        requestNew = requestNew + str(requestSplit[i]) + ' OR '
    print(requestNew)
    with index.searcher() as searcher:
        parser = QueryParser("description", index.schema)#description,搜索域
        myquery = parser.parse(requestNew)
        results = searcher.search(myquery, limit=20)  # limit为搜索结果的限制，默认为10
        for result1 in results:
            # print(dict(result1))
            new_list.append(dict(result1))
            name_list.append(dict(result1)['name'])
            catalog_list.append(dict(result1)['catalog'])
            description_list.append(dict(result1)['description'])
    # print(new_list)
    # print(name_list)
    # print(catalog_list)
    # print(description_list)
    return name_list,catalog_list,description_list


if __name__ == '__main__':
    get_indexSearching_result("A internet web service based on GPS")