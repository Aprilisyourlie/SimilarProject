from django.shortcuts import render
import IndexSearching.indexSearching as indexSearching

# Create your views here.

# 处理并传递数据的函数


def result(request):
    user_text = request.GET['text']
    namelist,cataloglist,descriptionlist = indexSearching.get_indexSearching_result(user_text)
    return render(request, 'result.html', {'catalog': cataloglist, 'name': namelist, 'description': descriptionlist})
