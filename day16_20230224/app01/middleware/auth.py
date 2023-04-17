from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleWare(MiddlewareMixin):
    """ 中间件 """

    def process_request(self, request):
        # 0.排除不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前用户的session信息，如果能读取到，说明用于已经登录，可以继续往下走。
        info_dict = request.session.get("info")
        print(info_dict)
        if info_dict:
            return

        # 2.如果没有登陆过，就返回登录页面
        return redirect('/login/')
