from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import PrettyModelForm, PrettyEditModelForm


def prettynum_list(request):
    """ 靓号列表  """

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 引入分页插件
    from app01.utils.pagination import Pagination

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,
        "queryset": page_queryset,  # 分页的数据
        "page_string": page_string,  # 页码
    }
    # 1.根据用户想要访问的页码，计算出起止位置,默认是1
    # page = int(request.GET.get('page', 1))
    # page_size = 10  # 每页显示十条数据
    # start = (page - 1) * page_size
    # end = page * page_size
    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[start:end]

    # # 数据总条数
    # total_count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    #
    # # 总页码，使用divmod(商，余数）
    # total_page_count, div = divmod(total_count, page_size)
    # if div:
    #     total_page_count += 1

    # # 计算出，显示当前页的前5页和后5页
    # plus = 5
    # if total_page_count <= 2 * plus + 1:
    #     # 数据库里面数据小于11页
    #     start_page = 1
    #     end_page = total_page_count
    # else:
    #     # 数据库的数据比较多
    #     # 当页数<5时（小极值）
    #     if page <= plus:
    #         start_page = 1
    #         end_page = 2 * plus + 1
    #     else:
    #         # 当前页 > 5
    #         # 当前页 + 5 > 总页数
    #         if (page + plus) > total_page_count:
    #             start_page = total_page_count - 2 * plus
    #             end_page = total_page_count
    #         else:
    #             start_page = page - plus
    #             end_page = page + plus + 1
    #
    # # 页码
    # page_str_list = []
    #
    # # 首页
    # page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    #
    # # 上一页
    # if page > 1:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    # else:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    # page_str_list.append(prev)
    #
    # # 页面
    # for i in range(start_page, end_page + 1):
    #     # 当前页码加上active样式
    #     if i == page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    #
    # # 下一页
    # if page < total_page_count:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    # else:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(1)
    # page_str_list.append(prev)
    #
    # # 尾页
    # page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))
    #
    # search_string = """
    #             <li>
    #                 <form style="float: left;margin-left: -1px" method="get">
    #                         <input style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
    #                                type="text" name="page" class="form-control" placeholder="页码">
    #                         <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
    #                 </form>
    #             </li>
    #         """
    # page_str_list.append(search_string)
    #
    # # 使用mark_safe包裹一层，显示得就是数字页面，而不是对象。
    # page_string = mark_safe("".join(page_str_list))
    return render(request, 'prettynum_list.html', context)


def prettynum_add(request):
    """  添加靓号 """
    # 如果是GET请求，先把
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'prettynum_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 如果判断输入有效，存储数据到数据库
        form.save()
        return redirect('/prettynum/list/')
    # 如果校验失败（在页面显示错误信息），返回添加页面，并且保留用户的输入
    return render(request, 'prettynum_add.html', {'form': form})


def prettynum_edit(request, nid):
    """  编辑靓号 """
    # 先获取要编辑的id的信息（对象）
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    # 判断请求调用方法，如果是get，返回编辑页面
    if request.method == "GET":
        # 根据ID，去数据库获取该行用户信息
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'prettynum_edit.html', {"form": form})

    # 如果是POST请求，提交数据，首先将数据存入到form
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list')
    return render(request, 'prettynum_edit.html', {"form": form})
