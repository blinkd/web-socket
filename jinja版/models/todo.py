from models import Model
import time
from utils import formatted_time

class Todo(Model):
    """
    继承自 Model 的 Todo 类
    """
    def __init__(self, form):
        super().__init__(form)
        self.task = form.get('task', '')
        self.completed = False
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('create_time', int(time.time()))
        self.updated_time = form.get('updated_time', '')

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()

    @classmethod
    def add(cls, form, user_id):
        t = Todo.new(form)
        t.user_id = user_id
        t.updated_time = int(time.time())
        t.save()

    @classmethod
    def new(cls, form, user_id=-1):
        form['user_id'] = user_id
        m = super().new(form)
        t = int(time.time())
        m.created_time = t
        m.updated_time = t
        m.save()
        return m

    @classmethod
    def complete(cls, id, completed):
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

    def formatted_created_time(self):
        return formatted_time(self.created_time)

    def formatted_updated_time(self):
        return formatted_time(self.updated_time)
