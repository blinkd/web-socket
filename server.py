import socket


def log(*args, **kwargs):
    # 用log函数代替print
    print('log', *args, **kwargs)


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 233 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = '{}\r\n{}'.format(header, body)
    return r.encode()


def html_content(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def route_message():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 233 OK\r\nContent-Type: text/html\r\n'
    body = html_content('html_basic.html')
    r = '{}\r\n{}'.format(header, body)
    return r.encode()


def route_image():
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    with open('funny.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        image = header + f.read()
        return image


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/': route_index,
        '/message': route_message,
        '/doge.gif': route_image,
    }
    response = r.get(path, error)
    return response()


def run(host, port):
    # 启动服务器
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:

        s.bind((host, port))
        # 服务器绑定接口
        s.listen()
        # 允许套接字进行连接
        while True:
            connection, address = s.accept()
            # 等待连接 字节字符串
            request = b''
            buffer_size = 1024
            while True:
                r = connection.recv(buffer_size)
                request += r
                if len(r) < buffer_size:
                    break

            request = request.decode()
            log('ip and request, {}\n{}'.format(address, request))
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里先判断一下 split 得到的数据的长度
            parts = request.split()
            log('parts',parts)

            if len(parts) > 0:
                path = parts[1]
                response = response_for_path(path)
                # response = b'HTTP/1.1 233 VERY OK\r\nContent-Type:text/html\r\n\r\n<h1>Hello World!</h1>'

                connection.sendall(response)
            else:
                log("接收到了一个空请求")
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=3000,
    )
    run(**config)
