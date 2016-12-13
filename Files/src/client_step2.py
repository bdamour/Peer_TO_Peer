# coding: utf-8
from lib.Message import *

path_chunks_charlie = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\chunks\\charlie')


sock_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_Alice = get_IP("alice")
IP_Bob = get_IP("bob")
IP_Tracker = get_IP("tracker")

PORT_Alice = get_PORT("alice")
PORT_Bob = get_PORT("bob")
PORT_Tracker = get_PORT("tracker")

#Connecte au tracker pour avoir file info 
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
	chunks_count,filename_length,filename,chunk_list= DECODE_FILE_INFO(mess_ans)
	print("\nchunks_count\n",chunks_count)
	print("\nfilename\n",filename)
	print("\nchunk list\n",chunk_list)
	
	print("================== MAKE STANDARD =================")
	#ici ce n'est pas la forme "standard" comme avec get_chunks_list(),get_chunks_peers()
	chunks_list,chunks_peers = make_standard(chunk_list,PORT_Alice,PORT_Bob)
	print("\nchunks list\n",chunks_list)
	print("\nchunks peers\n",chunks_peers)

	ok = True
else:
	print("The answer is not a FILE_INFO")
	ok = False



if ok:
	sock_bob.connect((IP_Bob, PORT_Bob)) 
	sock_alice.connect((IP_Alice, PORT_Alice)) 
	#CODE DE CHARLIE STEP 1 = 2 with make_standard(chunk_list,PORT_Alice,PORT_Bob)

	i=0
	while i < chunks_count:
		#On définit le chunk que l'on veut !
		chunk_hash = chunks_list[i][1]
		print("Send request for chunk: ",chunk_hash)
		if not isinstance(chunks_peers[i][1],tuple):
			#test si il est seul
			if chunks_peers[i][1] == 'alice':
				send_Message(GET_CHUNK(chunk_hash),sock_alice)
				mess_chunk_ans = receive_Message(sock_alice)
				#TEST si le retour n'est pas une erreur
				msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
				if msg_type!=5:
					#ERROR
					print(chunk_hash," is not with alice: \t ! CHUNK NOT DOWNLOADED !")
				else:
					#MSG_TYPE = 5 ==> CHUNK
					chunk_hash,chunk_content_length,chunk_content = DECODE_CHUNK(mess_chunk_ans)
					file = open(path_chunks_charlie+'//'+chunk_hash+".bin","w+b")
					file.write(chunk_content)
					file.close()


			elif chunks_peers[i][1] == 'bob':
				send_Message(GET_CHUNK(chunk_hash),sock_bob)
				mess_chunk_ans = receive_Message(sock_bob)
				#TEST si le retour n'est pas une erreur
				msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
				if msg_type!=5:
					#ERROR
					print(chunk_hash," is not with bob: \t ! CHUNK NOT DOWNLOADED !")
				else:
					#MSG_TYPE = 5 ==> CHUNK
					chunk_hash,chunk_content_length,chunk_content = DECODE_CHUNK(mess_chunk_ans)
					file = open(path_chunks_charlie+'//'+chunk_hash+".bin","w+b")
					file.write(chunk_content)
					file.close()

		elif isinstance(chunks_peers[i][1],tuple):
			j=0
			while j < len(chunks_peers[i][1]):

				if chunks_peers[i][1][j] == 'alice':
					send_Message(GET_CHUNK(chunk_hash),sock_alice)
					mess_chunk_ans = receive_Message(sock_alice)
					#TEST si le retour n'est pas une erreur
					msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
					
					if msg_type!=5:
						#ERROR
						print(chunk_hash," is not with alice !")
					else:
						#MSG_TYPE = 5 ==> CHUNK
						chunk_hash,chunk_content_length,chunk_content = DECODE_CHUNK(mess_chunk_ans)
						file = open(path_chunks_charlie+'//'+chunk_hash+".bin","w+b")
						file.write(chunk_content)
						file.close()
						break
				

				elif chunks_peers[i][1][j] == 'bob':
					send_Message(GET_CHUNK(chunk_hash),sock_bob)
					mess_chunk_ans = receive_Message(sock_bob)
					#TEST si le retour n'est pas une erreur
					msg_type, msg_length = DECODE_HEADER(mess_chunk_ans)
					if msg_type!=5:
						#ERROR
						print(chunk_hash," is not with bob and alice: \t ! CHUNK NOT DOWNLOADED !")
					else:
						#MSG_TYPE = 5 ==> CHUNK
						chunk_hash,chunk_content_length,chunk_content = DECODE_CHUNK(mess_chunk_ans)
						file = open(path_chunks_charlie+'//'+chunk_hash+".bin","w+b")
						file.write(chunk_content)
						file.close()
						print("But chunk",chunk_hash," is with bob !")
						break
					
				j+=1

				
		i+=1
		
	print("!!!! DOWNLOAD IS OVER !!!!")
else:
	print("ERROR: IMPOSSIBLE TO READ MESSAGE BECAUSE IS NOT FILE_INFO ")

