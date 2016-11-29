#-*- coding :Latin -1 -*
import socket
import threading
import os
import glob
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 1337))
sock.listen()

def handle_client(client_sock, client_addr):
	while True:
		msg = client_sock.recv(1024).decode("utf-8")
		if len(msg) == 0:
			client_sock.close()
		break
	print("%s:%d> %s" % (client_addr[0], client_addr[1], msg))
	client_sock.send(msg[::-1].encode("utf-8"))


while True:
	client_sock, client_addr = sock.accept()
	th = threading.Thread(target=handle_client, args=(client_sock,client_addr))
	th.daemon = True
	th.start()

os.system("pause")

