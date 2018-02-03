import socket

s = socket.socket()

host = 'localhost'
port = 2000

s.connect((host, port))
# 连接到服务器的地址端口
ip, port = s.getsockname()
print('本机 ip 和 port {} {}'.format(ip, port))

http_request = 'GET / HTTP/1.1\r\nHost:{}\r\nUser-Agent: xxxxxx \r\n\r\n'.format(host)

request = http_request.encode()
print('请求', request)
s.send(request)
# 发送请求
response = s.recv(1023)

print('响应',response)

print('响应的 str 格式\n{}'.format(response.decode()))
