import socket
import _thread

from request import Request
from utils import log

from routes import error


from routes.routes_todo import route_dict as todo_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_static import route_dict as static_routes


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    # 注册外部的路由
    r.update(todo_routes())
    r.update(weibo_routes())
    r.update(user_routes())
    r.update(static_routes())
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
