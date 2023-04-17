from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        # }


class PrettyModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}+$', '数字必须以159开头')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["id", "mobile", "price", "level", "status"]

    # 验证：方式2
    def clean_mobile(self):
        text_mobile = self.cleaned_data["mobile"]

        # 判断号码是否存在
        exists = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入值返回
        return text_mobile


class PrettyEditModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}+$', '数字必须以159开头')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    # 验证：手机号码存在且不等于自己
    def clean_mobile(self):
        # 当前编辑的那一行的ID
        # print(self.instance.pk)

        text_mobile = self.cleaned_data["mobile"]

        # 判断号码是否存在,排除当前编辑行的ID
        exists = models.PrettyNum.objects.exclude(self.instance.pk).filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入值返回
        return text_mobile
