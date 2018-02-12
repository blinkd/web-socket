import json

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        log('models', models)

        first_index = 0
        if self.id is None:
            log('id is None')
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                log('first index', first_index)
                self.id = first_index

            models.append(self)
        else:
            log('id is not None')
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)