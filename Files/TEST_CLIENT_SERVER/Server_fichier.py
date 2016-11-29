#-*- coding :Latin -1 -*
import socket
import threading
import os
import glob
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 1337))
sock.listen()

def handle_chunk(client_sock,client_addr):
	#Gestion du fichier
	msg = client_sock.recv(1024).decode("utf-8")
	if msg == "test":
		path = glob.glob("*.bin")
		print(path)
		size = os.path.getsize(path[0])
		
		if size > 1024:  # on envoit par paquet !
			print("Size of file {}".format(size))
			fichier = open(path[0],"rb")	
			
			client_sock.send(str(size).encode("utf-8"))
			#Le serveur attend que le client soit prêt pour envoyer les paquets
			instruction_client = client_sock.recv(1024).decode("utf-8")
			if instruction_client == "PRET":
				client_sock.send("OK".encode("utf-8"))
				

			print("DEBUT OPERATION")
			num = 0
			for i in range(size//1024): #On parcourt tous les paquets  (division euclidienne //)
				fichier.seek(num, 0) # on se deplace par rapport au numero de caractere (de 1024 a 1024 octets)
				donnees = fichier.read(1024) # Lecture du fichier en 1024 octets
				client_sock.send(donnees) # Envoi du fichier par paquet de 1024 octets
				num = num + 1024
				print("Send packet {}".format(i))

			#Ici on envoit le dernier paquet
			print("Tous les paquets envoyés")
			fichier.seek(num - (num-size%1024), 0)
			donnees = fichier.read(size%1024)
			client_sock.send(donnees)
			print("Send last packet")

			client_sock.send("END".encode("utf-8"))
			print("FIN OPERATION")
			fichier.close()
	else:
		client_sock.send("ERROR NOT TEST".encode("utf-8"))



while True:
	client_sock,client_addr = sock.accept()
	print("Un client s'est connecté")
	"""th = threading.Thread(target=handle_chunk, args=(client_sock,client_addr))
	th.daemon = True
	th.start()"""
	handle_chunk(client_sock,client_addr)

os.system("pause")