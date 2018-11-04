from django.shortcuts import render
import IndexSearching.indexSearching as indexSearching

# Create your views here.

# 处理并传递数据的函数


def result(request):
    user_text = request.GET['text']
    result = [{},{},{},{},{},{},{},{},{},{}]
    namelist,cataloglist,descriptionlist = indexSearching.get_indexSearching_result(user_text)

    for i in range(10):
        result[i] = {'name':namelist[i]}
    for i in range(10):
        result[i]['catalog'] = cataloglist[i]
    for i in range(10):
        result[i]['description'] = descriptionlist[i]
    print(result)
    # resultlist = {'catalog': cataloglist, 'name': namelist, 'description': descriptionlist}
    # print(resultlist)
    return render(request, 'result.html',{'result':result})
