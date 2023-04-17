import json
import random
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm

datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin_id"]


def order_list(request):
    form = OrderModelForm()
    return render(request, "order_list.html", {"form": form})


@csrf_exempt
def order_add(request):
    """ 新建订单（Ajax请求） """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # title=? price=? status=? admin_id=?
        # 额外增加一些不是用户输入的值（自己计算出来的）
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 固定设置管理员ID，去哪里获取？seesion
        # form.instance.admin_id = 当前登录系统的管理员ID
        form.instance.admin_id = request.session["info"]["id"]
        # 保存到数据库中
        form.save()
        # return HttpResponse(json.dumps({"status": True}))
        return JsonResponse({"status": True})

    return JsonResponse({"status": True, 'error': form.errors})
