#-*- coding :Latin -1 -*
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(("localhost", 1337))

while True:
	msg = input("> ")
	sock.send(msg.encode("utf-8"))
	time.sleep(1)
	res = sock.recv(1024).decode("utf-8")
	if len(res) == 0:
		sock.close()
		break
	print("Server> %s" % res)