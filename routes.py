from utils import log
from models.message import Message
from models.user import User

import random

def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    username = request.cookies.get('username', '【游客】')
    return username


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode()


def response_with_headers(headers):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.x 210 VERY OK\r\n'
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            headers['Set-Cookie'] = 'user={}'.format(u.username)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = '{}\r\n{}'.format(header, body)
    log('login 的响应', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    """
    主页的处理函数, 返回主页的响应
    """
    log('本次请求的 method', request.method)
    # if request.method == 'POST':
    #     data = request.form()
    # else:
    #     data = request.query

    form = request.query
    if len(form) > 0:
        m = Message.new(form)
        log('post', form)
        m.save()

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('messages.html')
    ms = '<br>'.join([str(m) for m in Message.all()])
    body = body.replace('{{messages}}', ms)
    r = header + '\r\n' + body
    return r.encode()


def route_message_add(request):
    """
    主页的处理函数, 返回主页的响应
    POST /messages HTTP/1.1
    Host: localhost:3000
    Content-Type: application/x-www-form-urlencoded

    message=123&author=gua
    """
    log('本次请求的 method', request.method)
    form = request.form()
    m = Message.new(form)
    log('post', form)
    # 应该在这里保存 message_list
    m.save()

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('messages.html')
    ms = '<br>'.join([str(m) for m in Message.all()])

    body = body.replace('{{messages}}', ms)
    r = header + '\r\n' + body
    return r.encode()


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'dota.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/messages/add': route_message_add,
}
