from lib.Message import *

import threading,sys


def handle_client(client_socket,client_addr):
	
	while True:
		print("ENTER HANDLE CLIENT")
		#Recoit le message !
		try:
			Mess = receive_Message(client_socket)
			print("RECEIVE THE MESSAGE",Mess)
			#Verifie la requete
			if message_format(Mess) == -1:
				send_Message(ERROR(0),client_socket) #INVALID_MESSAGE_FORMAT
				print("ANSWER: INVALID_MESSAGE_FORMAT")
			elif message_format(Mess) != 4:  
				send_Message(ERROR(2),client_socket) #CHUNK_NOT_FOUND, 4 = GET_CHUNK
				print("ANSWER: CHUNK_NOT_FOUND")
			elif  message_format(Mess) == 4: #message_format(Message) == 4
				print("CHUNK_OK!")
				chunk_hash = DECODE_GET_CHUNK(Mess) #chunk_hash de type str
				print("RECEIVE REQUEST",chunk_hash)
				if Alice.is_chunk_present(chunk_hash):
					send_Message(CHUNK(chunk_hash,Alice.path_folder_chunk()),client_socket)
					print("CHUNK ",chunk_hash ,"EXIST => CHUNK SEND !")
				else:
					print("ERROR: CHUNK ",chunk_hash," NOT FOUND")
					send_Message(ERROR(2),client_socket) #CHUNK_NOT_FOUND, 4 = GET_CHUNK
				
		except:
			print("CONNECTION ALICE ABORTED")
			break
			


#Take the IP and PORT
my_name = "alice"
Alice = Peer(my_name)
Alice_IP = str(Alice.IP)
Alice_PORT = int(Alice.PORT)
print("Alice_IP : ",Alice_IP,"\tAlice_PORT : ",Alice_PORT)

#Create the server
sock_alice = init_server(Alice_IP,Alice_PORT)
sock_alice.listen(5)


while True:
	client_socket,client_addr = sock_alice.accept()
	print(my_name,": ACCEPT")
	th = threading.Thread(target=handle_client,args=(client_socket,client_addr))
	th.daemon = True
	th.start()
	print("=========== START SERVER ===========")
	