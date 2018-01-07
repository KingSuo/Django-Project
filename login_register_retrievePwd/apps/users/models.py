# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name=u'昵称', default='', null=True, blank=True)
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=6, verbose_name=u'性别', choices=(('male', u'男'), ('female', u'女')), default='mela')
    address = models.CharField(max_length=100, verbose_name=u'地址', default='', null=True, blank=True)
    mobile = models.CharField(max_length=11, verbose_name=u'手机', default='', null=True, blank=True)
    image = models.ImageField(max_length=100, verbose_name=u'头像', upload_to='image/%Y/%m', default='image/default.png', null=True, blank=True)
    last_sendTime = models.DateTimeField(verbose_name=u'最近一次发送邮件时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=8, verbose_name=u'发送类型', choices=(('register', u'注册'), ('retrieve', u'找回')), default='retrieve')
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)
    dispose_time = models.DateTimeField(verbose_name=u'被处理时间', default=datetime.now)   # 用户点击激活链接的时间
    is_effective = models.BooleanField(verbose_name=u'验证码生效', default=False)   # 验证码是否生效

    class Meta:
        verbose_name = u'邮箱验证'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.code, self.email)
