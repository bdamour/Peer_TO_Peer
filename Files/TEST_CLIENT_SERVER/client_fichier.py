#-*- coding :Latin -1 -*
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(("localhost", 1337))

while True:
	msg = input("> ")
	sock.send(msg.encode("utf-8"))
	#On recoit le nombre de paquet à recevoir
	size = sock.recv(1024).decode("utf-8")
	size = int(size)
	print("Le fichier a une taille {}. Debut de l'opération !".format(size))

	#On connait la taille du fichier qui va être envoyé, on crée donc un fichier qu'on va remplir
	mon_fichier = open("copie.bin","a+b")
	sock.send("PRET".encode("utf-8"))

	reponse = sock.recv(1024).decode("utf-8")
	while reponse != "OK":
		print("Reponse != OK")

	#Debut de l'operation
	#donnes = ""
	i=0
	donnes = sock.recv(1024)	
	while True:	
		if donnes != "END".encode("utf-8"):
			mon_fichier.write(donnes)
			print("Packet recu {}".format(i))
			i+=1
		else:
			mon_fichier.write(donnes)
			print("Fichier recu !")
			break
		donnes = sock.recv(1024)

	print("Fichier recu !")			
	mon_fichier.close()
	
	

	




	#remove("copie.bin")

	"""
	res = sock.recv(1024).decode("utf-8")
	print(res)

	if len(res) == 0:
		sock.close()
		break
	print("Server> %s" % res)
	"""