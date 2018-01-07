# -*- coding:utf-8 -*-
__author__ = 'kingsuo'
__date__ = '2017/12/29 21:15'


import xadmin
from xadmin import views

from .models import EmailVerifyRecord


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = u'King Suo 后台管理系统'
    site_footer = u'King Suo 后台管理网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
