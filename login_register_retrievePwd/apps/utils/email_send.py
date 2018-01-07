# -*- coding:utf-8 -*-
__author__ = 'kingsuo'
__date__ = '2017/12/30 20:15'

import random
from datetime import datetime

from django.core.mail import send_mail

from login_register_retrievePwd.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def generate_code_str(str_length=8):
    str_bank = 'zxcvbnmaertyuiopsdfghjkl7890ZXCVBNMAqw123456SDFGHJKLPOIUYTREWQ'
    code_str = ''
    for i in range(str_length):
        code_str += str_bank[random.randint(0, (len(str_bank)-1))]

    return code_str


def send_email(email, send_type='register'):
    code = generate_code_str(16)
    email_record = EmailVerifyRecord()
    email_record.email = email
    email_record.send_type = send_type
    email_record.code = code
    # email_record.send_time = datetime.now()
    email_record.save()

    if send_type == 'register':
        email_title = u'注册信息'
        email_body = u'请点击下面链接来激活你的注册信息，链接有效时间为10分钟：\nhttp://127.0.0.1:8000/active/%s' % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        return send_status
    elif send_type == 'retrieve':
        email_title = u'密码找回'
        email_body = u'请点击下面链接来重置你的密码：http://127.0.0.1:8000/retrieve/%s' % code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        return send_status
