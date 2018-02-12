from models.todo import Todo
from routes import (
    redirect,
    template,
    response_with_headers,
)


def index(request):
    """
    todo 首页的路由函数
    """

    todo_list = Todo.all()
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
    form = request.form()
    t = Todo.new(form)
    t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')



def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/todo': index,
        '/todo/add': add,
        '/todo/edit': edit,
        '/todo/update': update,
        '/todo/delete': delete,
    }
    return d