from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from io import BytesIO
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="图片验证码",
        widget=forms.TextInput,
        required=True
    )

    # 用户输入密码为明文，需要进行md5加密，然后与数据库进行匹配
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    """ 登录 """

    # 检查用户是否登录，已登录继续往下走；未登录，跳转回登录页面
    # 用户发来请求，获取cookie字符串，拿着随机字符串看看session中有有没有

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到用户名和密码
        # {'username': 'wupeiqi', 'password': '123', 'code': '123'}

        # 验证码的校验
        # 使用pop的原因是要剔除掉验证码，后续与数据库中数据进行比较时只需要username和password
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 用MD5值去进行数据库校验是否正确,获取用户对象，None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        print(admin_object)
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户密码正确
        # 网站要生成一个随机字符串，写到用户浏览器cookie中，再写入到session中：
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # session用户信息保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list/")

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成验证码图片 """

    # 调用pillow函数生成图片
    img, code_string = check_code()

    # 写入到自己的session中 （以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string

    # 设置验证码60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/login/')
