import ssl
import socket


def parsed_url(url):

    # 解析 url 返回 (protocol host port path)
    # 检查协议
    if url[:7] == 'http://':
        u = url.split('://')[1]
        protocol = 'http'
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        protocol = 'http'
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    i = host.find(':')
    if i == -1:
        # 检查端口
        port_dict = {
            'http': 80,
            'https': 443,
        }
        # 默认端口
        port = port_dict[protocol]
    else:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def parsed_response(r):
    """
    解析出 状态码 headers body
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body


def response_by_socket(s):

    # 返回socket 读取的所有数据

    response = b''
    buffer_size = 1024
    while True:
        print('new loop')
        r = s.recv(buffer_size)
        print('response', len(r), r)
        response += r
        if len(r) < buffer_size:
            return response


def socket_by_protocol(protocol):
    s = socket.socket()
    if protocol == 'https':
        return ssl.wrap_socket(s)
    else:
        return s


def get(url):

    protocol, host, port, path = parsed_url(url)
    print('log request', protocol, host, port, path)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\n\r\n'.format(path, host)
    s.send(request.encode())

    response = response_by_socket(s)
    r = response.decode()
    # print('response:\n', r)
    status_code, headers, body = parsed_response(r)

    if status_code == 301:
        url = headers['Location']
        return get(url)
    else:
        return response, status_code


def main():
    url = 'http://movie.douban.com/top250'
    response, status_code = get(url)
    print(response.decode())


if __name__ == '__main__':
    main()
