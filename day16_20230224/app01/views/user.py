from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm


def user_list(request):
    """ 用户管理 """

    # 获取所有的用户表
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    """  添加用户 """
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 将数据提交到数据库
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender_id, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")


def user_model_form_add(request):
    """  添加用户（ModelForm版本 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect("/user/list/")
    # 校验失败（在页面显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """  编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()
    # if request.method == "GET":
    #     # 根据nid,获取它的数据
    #     row_object = models.Department.objects.filter(id=nid).first()
    #     return render(request, "user_edit.html", {"row_object": row_object})
    #
    # # 获取用户提交的标题
    # title = request.POST.get("title")
    #
    # # 根据ID找到数据库中的数据并进行更新
    # models.Department.objects.filter(id=nid).update(title=title)
    #
    # # 重定向部门列表
    # return redirect("/depart/list/")
    if request.method == "GET":
        # 根据ID去数据库里面获取要编辑的那一行数据(对象）
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存用户输入的所有数据，如果想要在用户输入之外再增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    """  删除部门 """
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 返回重定向
    return redirect("/user/list/")
