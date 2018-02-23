import random

from jinja2 import Environment, FileSystemLoader
import os.path
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)


def configured_environment():
    # __file__ 就是本文件的名字
    # 得到用于加载模板的目录
    path = '{}/templates/'.format(os.path.dirname(__file__))
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    return Environment(loader=loader)


class JinjaEnvironment:

    # todo 改成类
    env = configured_environment()


def template(path, **kwargs):
    t = JinjaEnvironment.env.get_template(path)
    return t.render(**kwargs)


def formatted_time(unixtime):
    dt = time.localtime(unixtime)
    ds = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return ds
