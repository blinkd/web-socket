from models import Model

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
    def guest(cls):
        form = dict(
            id=-1,
            username='【游客】',
        )
        u = User.new(form)
        return u
