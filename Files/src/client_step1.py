# coding: utf-8
from lib.Message import *


sock_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_Alice = get_IP("alice")
IP_Bob = get_IP("bob")
PORT_Alice = get_PORT("alice")
PORT_Bob = get_PORT("bob")

sock_bob.connect((IP_Bob, PORT_Bob)) 
sock_alice.connect((IP_Alice, PORT_Alice)) 
path_chunks_charlie = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\chunks\\charlie')


#Fonction pour Charlie
filename,chunks_count = get_description()
chunks_list = get_chunks_list()
chunks_peers = get_chunks_peers()

print("filename\t\n", filename)
print("chunks_count\t\n",chunks_count)

print("chunks_list\t\n",chunks_list)
print("chunks_peers\t\n",chunks_peers)



#CODE DE CHARLIE STEP 1

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
sock_alice.close()
sock_bob.close()


