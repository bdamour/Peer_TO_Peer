# coding: utf-8
from lib.Message import *

path_chunks_charlie = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\chunks\\charlie')


sock_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



#Broadcast the tracker
addr = ('255.255.255.255',9000)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Send discover tracker")
UDPSock.sendto(Message_to_byte_array(DISCOVER_TRACKER()),addr)

print("réponse :\n")

ans = UDPSock.recvfrom(10000)
print(ans)

mess = byte_array_to_Message(ans[0])

IP_Tracker,PORT_Tracker,tracker_name_length,tracker_name = DECODE_TRACKER_INFO(mess)
print("ip_address",IP_Tracker)
print("port_number",PORT_Tracker)
print("tracker_name",tracker_name)


print("Connexion tracker")
sock_tracker.connect((IP_Tracker, PORT_Tracker))

#MAUVAIS MESSAGE 
send_Message(Message(12),sock_tracker)
print("Send request: NOTHING")

mess_ans = receive_Message(sock_tracker)
if message_format(mess_ans) == 3:
	print("The answer is a FILE_INFO\n")
	chunks_count,filename_length,filename,chunk_list= DECODE_FILE_INFO(mess_ans)
	print("\nchunks_count\n",chunks_count)
	print("\nfilename\n",filename)
	
	#ici ce n'est pas la forme "standard" comme avec get_chunks_list(),get_chunks_peers()
	chunks_list,chunks_peers = make_standard(chunk_list,PORT_Alice,PORT_Bob)
else:
	print("The answer is not a FILE_INFO")


#BON MESSAGE 
send_Message(GET_FILE_INFO(),sock_tracker)  
print("Send request: GET_FILE_INFO")

mess_ans = receive_Message(sock_tracker)
if message_format(mess_ans) == 3:
	print("The answer is a FILE_INFO\n")
	chunks_count,filename_length,filename,chunks_list= DECODE_FILE_INFO(mess_ans)
	print("\nchunks_count\n",chunks_count)
	print("\nfilename\n",filename)
	
	ok = True
else:
	print("The answer is not a FILE_INFO")
	ok = False



print("================ DEBUT DE L'EXTRACTION =================")
#On crée un liste contenant tous les ports possibles afin d'initialiser le bon nombre de socket
i=0
list_port = []
list_index_tuple = []
list_index_list = []

while i <chunks_count:
	if  isinstance(chunks_list[i][1],tuple):
		list_index_tuple.append(i)   #l'élément à la position i est seul, => un seul peer
		port = chunks_list[i][1][1] #récupère le port
		ip = chunks_list[i][1][0] #Récupère l'ip dans la list
		if port in list_port:
			pass
		else:
			list_port.append(port)

	elif isinstance(chunks_list[i][1],list):
		list_index_list.append(i)
		#On parcourt donc la liste !!
		j=0
		while j < len(chunks_list[i][1]):
			port = chunks_list[i][1][j][1] #Récupère le port dans la list
			ip = chunks_list[i][1][j][0] #Récupère l'ip dans la list
			if port in list_port:
				pass
			else:
				list_port.append(port)
			j+=1
	i+=1



#On a initialisé autant de socket qu'il y a de port, peut parcourir list_index_tuple, et lis_index_list
#pour appliquer le traitement qu'il faut
nb_chunks =0
for index in list_index_tuple:
	#print(index)
	chunk_hash = chunks_list[index][0].decode("utf-8")
	ip = chunks_list[index][1][0] #récuèpe l'ip
	port = chunks_list[index][1][1] #récuèpe le port
	sock_to_discuss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock_to_discuss.connect((ip, port))

	#On possède maintenant le socket, le chunk, et l'ip
	send_Message(GET_CHUNK(chunk_hash),sock_to_discuss)
	mess_chunk_ans = receive_Message(sock_to_discuss)
	#TEST si le retour n'est pas une erreur
	msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
	if msg_type!=5:
		#ERROR
		print(chunk_hash," is not here \t ! CHUNK NOT DOWNLOADED !")
		
	else:
		#MSG_TYPE = 5 ==> CHUNK
		
		chunk_hash,chunk_content_length,chunk_content = DECODE_CHUNK(mess_chunk_ans)
		msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
		file = open(path_chunks_charlie+'//'+chunk_hash+".bin","w+b")
		file.write(chunk_content)
		file.close()
		nb_chunks+=1
		print(chunk_hash," is  here \t ! CHUNK  DOWNLOADED !")
		#print("msg_length",4*msg_length,"chunk content_length",chunk_content_length,"content_length_computation",len(chunk_content))

print("!!!! DOWNLOAD TUPLE IS OVER !!!!")

for index in list_index_list:
	#print(index)
	chunk_hash = chunks_list[index][0].decode("utf-8")

	for element in chunks_list[index][1]:
		ip = element[0] #récuèpe l'ip
		port = element[1] #récuèpe le port
		sock_to_discuss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock_to_discuss.connect((ip, port))

		#On possède maintenant le socket, le chunk, et l'ip
		send_Message(GET_CHUNK(chunk_hash),sock_to_discuss)
		mess_chunk_ans = receive_Message(sock_to_discuss)
		#TEST si le retour n'est pas une erreur
		msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
		if msg_type!=5:
			#ERROR
			print(chunk_hash," is not here \t ! CHUNK NOT DOWNLOADED !")
			
		else:
			#MSG_TYPE = 5 ==> CHUNK
			chunk_hash,chunk_content_length,chunk_content = DECODE_CHUNK(mess_chunk_ans)
			msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
			
			file = open(path_chunks_charlie+'//'+chunk_hash+".bin","w+b")
			file.write(chunk_content)
			file.close()
			nb_chunks+=1
			print(chunk_hash," is  here \t ! CHUNK  DOWNLOADED !")
			#print("msg_length",4*msg_length,"chunk content_length",chunk_content_length,"content_length_computation",len(chunk_content))
			break
			

print("!!!! DOWNLOAD LIST IS OVER !!!!")

print("TOTAL CHUNK DOWNLOADED : " ,nb_chunks, "and the total of chunk was :", chunks_count, "Have all ?", nb_chunks==chunks_count)