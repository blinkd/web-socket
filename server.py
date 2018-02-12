import socket
import urllib.parse

from utils import log

from routes import route_static, error
from routes import route_dict
from routes_todo import route_dict as routes_todo

import _thread


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self, raw_data):
        header, self.body = raw_data.split('\r\n\r\n', 1)
        h = header.split('\r\n')

        parts = h[0].split()
        self.method = parts[0]
        path = parts[1]
        self.path = ''
        self.query = {}
        self.parsed_path(path)
        log('Request: path 和 query', self.path, self.query)

        self.headers = {}
        self.cookies = {}
        self.add_headers(h[1:])
        self.add_cookies()
        log('Request: headers 和 cookies', self.headers, self.cookies)

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

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

    def parsed_path(self, path):
        index = path.find('?')
        if index == -1:
            self.path = path
            self.query = {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            self.path = path
            self.query = query


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    r.update(route_dict)
    r.update(routes_todo())
    response = r.get(request.path, error)
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
            log('ip {}'.format(address))
            _thread.start_new_thread(process_request,(address,connection))


def process_request(address,connection):
    r = connection.recv(1024)
    r = r.decode()
    log('ip 和 request, {}\n{}'.format(address, r))
    log('request log:\n'.format(r))
    request = Request(r)
    # request.raw_data = r
    # header, request.body = r.split('\r\n\r\n', 1)
    # h = header.split('\r\n')
    # parts = h[0].split()
    # request.path = parts[1]
    # # 设置 request 的 method
    # request.method = parts[0]
    # # 用 response_for_path 函数来得到 path 对应的响应内容
    # request.add_headers(h[1:])
    response = response_for_path(request)
    log("response log:\n", response)
    # 把响应发送给客户端
    connection.sendall(response)

    # 处理完请求, 关闭连接
    connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    run(**config)
