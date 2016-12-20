# TRACKER step 2 

from lib.Message import *
import threading

#FONCTION COTE SERVEUR
def handle_charlie(charlie_socket,charlie_addr):
	while True:
		print("ENTER HANDLE CHARLIE")
		#Recoit le message !
		try:
			Mess = receive_Message(charlie_socket)
			print("RECEIVE THE MESSAGE",Mess)
			#Verifie la requete
			if message_format(Mess) == -1:
				send_Message(ERROR(0),charlie_socket) #INVALID_MESSAGE_FORMAT
				print("ANSWER: INVALID_MESSAGE_FORMAT")
			elif message_format(Mess) != 2:  
				send_Message(ERROR(1),charlie_socket) #INVALID_REQUEST, 1  
				print("ANSWER: INVALID_REQUEST")
			elif  message_format(Mess) == 2: #message_format(Message) == 2 => GET_FILE_INFO()
				print("FILE_INFO_OK!")
				send_Message(FILE_INFO(),charlie_socket)
				
		except :
			print("CONNECTION TRACKER ABORTED")
			break



#Take the IP and PORT
my_name = "tracker"
Tracker = Peer(my_name)
Tracker_IP = str(Tracker.IP)
Tracker_PORT = int(Tracker.PORT)
print("Tracker_IP : ",Tracker_IP,"\tTracker_PORT : ",Tracker_PORT)

#Create the server
sock_tracker = init_server(Tracker_IP,Tracker_PORT)
sock_tracker.listen(5)


while True:
	charlie_socket,charlie_addr = sock_tracker.accept()
	print(my_name,": ACCEPT")
	th = threading.Thread(target=handle_charlie,args=(charlie_socket,charlie_addr))
	th.daemon = True
	th.start()
	print("=========== START SERVER ===========")