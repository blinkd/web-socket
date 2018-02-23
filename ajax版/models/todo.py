import time

from models import Model
from utils import formatted_time


class Todo(Model):
    """
    针对我们的数据 TODO
    我们要做 4 件事情
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据

    Todo.new() 来创建一个 todo
    """

    def __init__(self, form):
        super().__init__(form)
        self.task = form.get('task', '')
        self.completed = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        # 默认不关联任何用户
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')

    @classmethod
    def new(cls, form):
        m = super().new(form)
        t = int(time.time())
        m.created_time = t
        m.updated_time = t
        m.save()
        return m

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

    def formatted_created_time(self):
        return formatted_time(self.created_time)

    def formatted_updated_time(self):
        return formatted_time(self.updated_time)
