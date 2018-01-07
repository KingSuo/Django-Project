# _*_ encoding: utf-8 _*_
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from utils.email_send import send_email
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm

# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form:
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'base.html')
                else:
                    return render(request, 'login.html', {'msg': u'用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': u'用户名或密码错误！', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            user_email = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            if UserProfile.objects.filter(email=user_email):
                user_profile = UserProfile.objects.get(email=user_email)
                if user_profile.is_active:
                    return render(request, 'register.html', {'msg': u'该邮箱已注册！', 'register_form': register_form, 'forgetPwd': u'忘记密码？'})
                else:
                    delta_time = datetime.now() - user_profile.last_sendTime
                    if delta_time.seconds >= 60:  # 时间间隔大于60s可再次发送激活邮件
                        send_status = send_email(email=user_email, send_type='register')
                        if send_status:
                            user_profile.last_sendTime = datetime.now()  # 更新最近一次发送激活邮件时间
                            user_profile.username = u'用户(%s)' % user_name
                            user_profile.email = user_email
                            user_profile.password = make_password(pass_word)
                            user_profile.save()

                            return render(request, 'register.html', {'msg': u'激活邮件已发送，请到邮箱完成激活注册！', 'register_form': register_form})
                        else:
                            return render(request, 'register.html', {'msg': u'激活邮件发送失败，请重新点击注册！', 'register_form': register_form})
                    else:
                        return render(request, 'register.html', {'msg': u'激活邮件已发送，勿重复发送！请前往邮箱完成激活注册', 'register_form': register_form})
            else:
                send_status = send_email(email=user_email, send_type='register')
                if send_status:
                    user_profile = UserProfile()
                    user_profile.last_sendTime = datetime.now()
                    user_profile.is_active = False
                    user_profile.username = u'用户(%s)' % user_name
                    user_profile.email = user_email
                    user_profile.password = make_password(pass_word)
                    user_profile.save()

                    return render(request, 'register.html', {'msg': u'激活邮件已发送，请到邮箱完成激活注册！', 'register_form': register_form})
                else:
                    return render(request, 'register.html', {'msg': u'邮件发送失败，请重新点击注册激活！', 'register_form': register_form})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        if EmailVerifyRecord.objects.filter(code=active_code):
            email_verify_record = EmailVerifyRecord.objects.get(code=active_code)
            email = email_verify_record.email
            send_time = email_verify_record.send_time # 用户收到激活链接的时间
            dispose_time = datetime.now()   # 用户点击激活链接的时间
            email_verify_record.dispose_time = dispose_time    # 用户点击激活链接的时间同步到数据库中
            delta_time = dispose_time - send_time    # 用户从收到激活链接到点击链接的时间间隔
            if delta_time.seconds >= 600:    # 间隔时间超过600s，链接失效
                email_verify_record.is_effective = False
                email_verify_record.save()
                return render(request, 'active_fail.html', {'msg': u'链接已超时失效，请重新获取链接！', 'email': email})
            else:
                email_verify_record.is_effective = True
                email_verify_record.save()
                user_profile = UserProfile.objects.get(email=email)
                user_profile.is_active = True
                user_profile.save()

            return render(request, 'active_success.html', {'username': user_profile.username, 'time': datetime.now()})
        else:
            return render(request, 'active_fail.html')


class ActiveFailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        return render(request, 'register.html', {'email': email})