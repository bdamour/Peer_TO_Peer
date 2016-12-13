# TRACKER step 2 

from lib.Message import *
import threading

#Take the IP and PORT
my_name = "tracker"
Tracker = Peer(my_name)
Tracker_IP = "127.0.0.1"
Tracker_PORT = 9000

#Create UDP server
UDPSock = init_UDP_server("",9000)



while True:
	print("ENTER BROADCAST ")

	try:
		charlie_socket,charlie_addr = UDPSock.recvfrom(1024)
		print("=========== START SERVER ===========")
		Mess = byte_array_to_Message(charlie_socket)
		print("RECEIVE THE MESSAGE",Mess)
		#Verifie la requete
		if message_format(Mess) == -1:
			send_Message(ERROR(0),charlie_socket) #INVALID_MESSAGE_FORMAT
			print("ANSWER: INVALID_MESSAGE_FORMAT")
		elif message_format(Mess) != 0:  
			send_Message(ERROR(1),charlie_socket) #INVALID_REQUEST, 1  
			print("ANSWER: CHUNK_NOT_FOUND")
		elif  message_format(Mess) == 0: #message_format(Message) == 0 => DISCOVER_TRACKER()
			print("DISCOVER_TRACKER_OK!")
			UDPSock.sendto(Message_to_byte_array(TRACKER_INFO(Tracker_IP,Tracker_PORT,my_name)),charlie_addr)
			print("MESSAGE SENT !")
			break
			
	except :
		print("CONNECTION TRACKER ABORTED")
		break
UDPSock.close()





def handle_charlie(charlie_socket,charlie_addr):
	while True:
		print("ENTER HANDLE CHARLIE")
		#Recoit le message !
		try:
			Mess = receive_Message(charlie_socket)
			print("RECEIVE THE MESSAGE",Mess)

			if message_format(Mess) == -1:
				send_Message(ERROR(0),charlie_socket) #INVALID_MESSAGE_FORMAT
				print("ANSWER: INVALID_MESSAGE_FORMAT")
			elif message_format(Mess) != 2:  
				send_Message(ERROR(1),charlie_socket) #INVALID_REQUEST, 1  
				print("ANSWER: CHUNK_NOT_FOUND")
			elif  message_format(Mess) == 2: #message_format(Message) == 2 => GET_FILE_INFO()
				print("FILE_INFO_OK!")
				send_Message(FILE_INFO(),charlie_socket)
				
		except :
			print("CONNECTION TRACKER ABORTED")
			sys.exit(1)
			break



#Create server
sock_tracker = init_server(Tracker_IP,Tracker_PORT)
sock_tracker.listen(5)


while True:
	charlie_socket,charlie_addr = sock_tracker.accept()
	print(my_name,": ACCEPT")
	th = threading.Thread(target=handle_charlie,args=(charlie_socket,charlie_addr))
	th.daemon = True
	th.start()
	print("=========== START SERVER ===========")

sock_tracker.close()