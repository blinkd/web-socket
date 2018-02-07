import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict

import _thread


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        body = urllib.parse.unquote(self.body)
        log('form', self.body)
        log('form', body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        log('form() 字典', f)
        return f


def error(code=404):
    """
    根据 code 返回不同的错误响应
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path,request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path 和 query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/static': route_static,
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('开始运行于', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        # 监听 接受 读取请求数据 解码成字符串
        s.listen()
        while True:
            connection, address = s.accept()
            _thread.start_new_thread(process_request,(address,connection))


def process_request(address,connection):
    r = connection.recv(1024)
    r = r.decode()
    log('ip 和 request, {}\n{}'.format(address, r))
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r) > 0:
        # 只能 split 一次，因为 body 中可能有换行
        # 把 body 放入 request 中
        request = Request()
        header, request.body = r.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        parts = h[0].split()
        path = parts[1]
        # 设置 request 的 method
        request.method = parts[0]
        # 用 response_for_path 函数来得到 path 对应的响应内容
        response = response_for_path(path, request)
        # 把响应发送给客户端
        connection.sendall(response)
    else:
        log('接收到了一个空请求')

    # 处理完请求, 关闭连接
    connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    run(**config)
