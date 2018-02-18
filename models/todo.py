from models import Model


class Todo(Model):
    """
    继承自 Model 的 Todo 类
    """
    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = Todo.find_by(id = todo_id)
        t.title = form['title']
        t.save()
