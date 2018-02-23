from models import Model
from models.user import User


class Comment(Model):
    """
    评论类
    """
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    @classmethod
    def new(cls, form, user_id):
        m = super().new(form)
        m.user_id = user_id
        m.save()
        return m

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    @classmethod
    def update(cls, form):
        content = form.get('content', '')
        comment_id = int(form.get('id', -1))
        w = Comment.find(comment_id)
        w.content = content
        w.save()
        return  w