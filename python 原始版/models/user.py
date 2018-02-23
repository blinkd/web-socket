from models import Model
from utils import random_string
from models.session import Session

# Model 是用于存储数据的基类


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def validate_login(username, password):
        u = User.find_by(username=username)
        return u is not None and u.password == password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    @classmethod
    def login(cls, form, headers):
        username = form.get('username')
        password = form.get('password')
        if User.validate_login(username, password):
            u = User.find_by(username=username)
            # 设置随机字符串当令牌使用
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            session_id = random_string()
            form = dict(
                session_id=session_id,
                user_id=u.id,
            )
            s = Session.new(form)
            s.save()
            headers['Set-Cookie'] = 'session_id={}'.format(
                session_id
            )
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
            u = User.guest()

        return u, result

    @classmethod
    def register(cls, form):
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
        return u, result

    @classmethod
    def guest(cls):
        form = dict(
            id=-1,
            username='【游客】',
        )
        u = User.new(form)
        return u
