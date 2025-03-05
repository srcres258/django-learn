from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string

def random_str(randomlength=8):
    """生成指定长度的随机字符串"""

    chars = string.ascii_letters + string.digits # 生成a-zA-Z0-9的字符串
    strcode = ''.join(random.sample(chars, randomlength)) # 生成随机的长度为 randomlength 的字符串

    return strcode

def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(8)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    match send_type:
        case 'register':
            email_title = '博客的注册激活链接'
            email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/users/active/{0}'.format(code)

            send_status = send_mail(email_title, email_body, '2023002089@link.tyut.edu.cn', [email])
            if send_status:
                pass

        case 'forget':
            email_title = '找回密码链接'
            email_body = '请点击下面的链接修改你的密码：http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)

            send_status = send_mail(email_title, email_body, '2023002089@link.tyut.edu.cn', [email])
            if send_status:
                pass