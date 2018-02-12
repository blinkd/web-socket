from models import Model


class Todo(Model):
    """
    继承自 Model 的 Todo 类
    """
    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
