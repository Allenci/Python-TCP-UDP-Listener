import socket

address = ('192.168.0.133', 12345)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg =  '{ "Serial": "A08888"}'
    value = msg.encode()
    if not value:
        break
    s.sendto(value, address)
