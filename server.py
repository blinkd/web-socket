import socket

host = '0.0.0.0'
port = 2000

s = socket.socket()
# 新建套接字
s.bind((host,port))
# 服务器绑定接口
s.listen()
# 允许套接字进行连接
while True:
    connection,address = s.accept()
    # 等待连接 字节字符串
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            break
    
    print('ip and request, {}\n{}'.format(address, request.decode()))
    
    response = b'HTTP/1.1 233 VERY OK\r\nContent-Type:text/html\r\n\r\n<h1>Hello World!</h1>'

    connection.sendall(response)
    
    connection.close()
