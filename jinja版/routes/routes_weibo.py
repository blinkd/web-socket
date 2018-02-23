from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    http_response,
    current_user,
    login_required,
)
from utils import template, log


# 微博相关页面
def index(request):
    author_id = int(request.query.get('user_id', -1))
    user = current_user(request)
    if author_id == -1:
        author_id = user.id

    weibos = Weibo.find_all(user_id=author_id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def new(request):
    body = template('weibo_new.html')
    return http_response(body)


def add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    w = Weibo.new(form)
    w.user_id = u.id
    w.save()
    return redirect('/weibo/index')


def delete(request):
    u = current_user(request)
    # 删除微博
    weibo_id = int(request.query.get('id', None))
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    # 生成一个 edit 页面
    body = template('weibo_edit.html', weibo_id=w.id, weibo_content=w.content)
    return http_response(body)


def update(request):
    u = current_user(request)
    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    w = Weibo.find(weibo_id)
    w.content = content
    w.save()
    # 重定向到用户的主页
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    c = Comment.new(form)
    c.user_id = u.id
    c.save()
    log('comment add', c, u, form)
    weibo = Weibo.find(id=int(form['weibo_id']))
    return redirect('/weibo/index?user_id={}'.format(weibo.user_id))


def route_dict():
    r = {
        '/weibo/index': login_required(index),
        '/weibo/new': login_required(new),
        '/weibo/edit': login_required(edit),
        '/weibo/add': login_required(add),
        '/weibo/update': login_required(update),
        '/weibo/delete': login_required(delete),
        # 评论功能
        '/comment/add': login_required(comment_add),
    }
    return r
