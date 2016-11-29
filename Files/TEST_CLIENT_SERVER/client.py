#-*- coding :Latin -1 -*
import socket
from Structure import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(("localhost", 1337))

res = sock.recv(4096)
version2, msg_type2,msg_length2 = decode_header(res)
print("Recu: version, msg_type,msg_length \t", version2, msg_type2,msg_length2)

chunck = sock.recv(msg_length2*1024) #Taille du fichier en kO
mon_fichier = open("copie.bin","w+b")
mon_fichier.write(chunck)
print("Fini!")