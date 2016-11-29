#-*- coding :Latin -1 -*
import socket
import threading
import os
from Structure import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 1337))
sock.listen()

def handle_client(client_sock, client_addr):
	while True:
		#On récupère la taille du chunck
		msg_length = os.path.getsize("6f354416d03786f7480c2546c655f07e852c91bc.bin")
		version = 1
		msg_type = 48
		print("version, msg_type,msg_length:\t", version, msg_type,msg_length)
		binary = encode_header(version, msg_type,msg_length)
		client_sock.send(binary)
		fichier = open("6f354416d03786f7480c2546c655f07e852c91bc.bin","r+b")
		chunck_content=fichier.read()
		

		client_sock.send(chunck_content)
		break
	print("Envoyé !")


while True:
	client_sock, client_addr = sock.accept()
	th = threading.Thread(target=handle_client, args=(client_sock,client_addr))
	th.daemon = True
	th.start()


os.system("pause")

