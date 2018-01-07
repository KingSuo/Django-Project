# -*- coding:utf-8 -*-
__author__ = 'kingsuo'
__date__ = '2017/12/29 22:24'

from django import forms

from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class ForgetForm(forms.Form):
    email = forms.CharField(required=True)
    # captcha = CaptchaField()


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    # captcha = CaptchaField()