from models.todo import Todo
from routes import current_user
from routes import (
    redirect,
    template,
    response_with_headers,
    error,
    login_required,
)

from utils import log


def index(request):
    """
    todo 首页的路由函数
    """
    u = current_user(request)
    todo_list = Todo.find_all(user_id=u.id)
    # 下面这行生成一个 html 字符串
    todo_html = """
    <h3>
        {} : {}
        <a href="/todo/edit?id={}">编辑</a>
        <a href="/todo/delete?id={}">删除</a>
    </h3>
    """
    todo_html = ''.join([
        todo_html.format(
            t.id, t.title, t.id, t.id
        ) for t in todo_list
    ])

    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)

    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def edit(request):

    body = template('todo_edit.html')

    todo_id = int(request.query['id'])
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    todo_title = t.title
    body = body.replace('{{todo_id}}', str(todo_id))
    body = body.replace('{{todo_title}}', todo_title)
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo')


def update(request):
    form = request.form()
    Todo.update(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    t = Todo.new(form)
    t.user_id = u.id
    t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def same_user_required(route_function):
    '''
    edit与update函数分别对应http协议get请求与post请求
    所以权限函数先判断request.method
    然后根据对应的请求格式取得todo_id
    然后判断继续或是重定向
    '''
    def f(request):
        if request.method == 'GET':
            todo_id = int(request.query['id'])
            t = Todo.find_by(id=todo_id)
            u = current_user(request)
            if u.id == t.user_id:
                return route_function(request)
            else:
                return redirect('/todo')
        else:
            form = request.form()
            todo_id = int(form['id'])
            t = Todo.find_by(id=todo_id)
            u = current_user(request)
            if u.id == t.user_id:
                return route_function(request)
            else:
                return redirect('/login')
    return f



def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo': login_required(index),
        '/todo/add': login_required(add),
        '/todo/edit': login_required(same_user_required(edit)),
        '/todo/update': login_required(same_user_required(update)),
        '/todo/delete': login_required(same_user_required(delete)),
    }
    return d