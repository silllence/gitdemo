import json
from django import forms
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
        }


def task_list(request):
    """ 任务列表 """
    # 1.去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by('-id')
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    page_string = page_object.html()
    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": queryset,
        "page_string": page_string,
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)

    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    # json_string = json.dumps(data_dict)
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    print(request.POST)

    # 1.用户发送过来的数据进行校验(ModelForm进行校验)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

    data_dict = {"status": True}
    # json_string = json.dumps(data_dict)
    return HttpResponse(json.dumps(data_dict))
