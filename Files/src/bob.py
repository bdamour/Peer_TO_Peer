from lib.Message import *
import threading,sys


def handle_client(client_socket,client_addr):
	while True:
		print("ENTER  HANDLE CLIENT")
		try:
			Mess = receive_Message(client_socket)
			print("RECEIVE THE MESSAGE",Mess)

			if message_format(Mess) == -1:
				send_Message(ERROR(0),client_socket) #INVALID_MESSAGE_FORMAT
				print("ANSWER: INVALID_MESSAGE_FORMAT")
			elif message_format(Mess) != 4:  
				send_Message(ERROR(2),client_socket) #CHUNK_NOT_FOUND, 4 = GET_CHUNK
				print("ANSWER: CHUNK_NOT_FOUND")
			elif  message_format(Mess) == 4: #message_format(Message) == 4
				print("CHUNK_OK!")
				chunk_hash = DECODE_GET_CHUNK(Mess) #chunk_hash  type str
				print("RECEIVE REQUEST",chunk_hash)
				if Bob.is_chunk_present(chunk_hash):
					send_Message(CHUNK(chunk_hash,Bob.path_folder_chunk()),client_socket)
					print("CHUNK ",chunk_hash ,"EXIST => CHUNK SEND !")
				else:
					print("ERROR: CHUNK ",chunk_hash," NOT FOUND")
					send_Message(ERROR(2),client_socket) #CHUNK_NOT_FOUND, 4 = GET_CHUNK
				
		except:
			print("CONNECTION BOB ABORTED")
			break


#Take the IP and PORT
my_name = "bob"
Bob = Peer(my_name)
Bob_IP = str(Bob.IP)
Bob_PORT = int(Bob.PORT)
print("Bob_IP : ",Bob_IP,"\tBob_PORT : ",Bob_PORT)

#Create the server for bob
sock_bob = init_server(Bob_IP,Bob_PORT)
sock_bob.listen(5)


while True:
	client_socket,client_addr = sock_bob.accept()
	print(my_name,": ACCEPT")
	th = threading.Thread(target=handle_client,args=(client_socket,client_addr))
	th.daemon = True
	th.start()
	print("=========== START SERVER ===========")