import sys
from lib.Message import *

if len(sys.argv) < 2:
    print('Error: missing step number')
    sys.exit(1)
step = int(sys.argv[1])

if step == 1:
    # Step 1
	path_chunks_charlie = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\chunks\\charlie') 

	sock_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	IP_Alice = get_IP("alice")
	IP_Bob = get_IP("bob")
	PORT_Alice = get_PORT("alice")
	PORT_Bob = get_PORT("bob")

	sock_bob.connect((IP_Bob, PORT_Bob)) 
	sock_alice.connect((IP_Alice, PORT_Alice)) 


	filename,chunks_count = get_descritpion()
	chunks_list = get_chunks_list()
	chunks_peers = get_chunks_peers()

	print("filename\t\n", filename)
	print("chunks_count\t\n",chunks_count)

	i=0
	nb = 0
	while i < chunks_count:
		#Define the chunk we want !
		chunk_hash = chunks_list[i][1]
		print("Send request for chunk: ",chunk_hash)
		if not isinstance(chunks_peers[i][1],tuple):
			#test if he is alone
			if chunks_peers[i][1] == 'alice':
				send_Message(GET_CHUNK(chunk_hash),sock_alice)
				mess_chunk_ans = receive_Message(sock_alice)
				#TEST if the answer is not an error
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
					nb+=1


			elif chunks_peers[i][1] == 'bob':
				send_Message(GET_CHUNK(chunk_hash),sock_bob)
				mess_chunk_ans = receive_Message(sock_bob)
				#TEST if the answer is not an error
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
					nb+=1

		elif isinstance(chunks_peers[i][1],tuple):
			j=0
			while j < len(chunks_peers[i][1]):

				if chunks_peers[i][1][j] == 'alice':
					send_Message(GET_CHUNK(chunk_hash),sock_alice)
					mess_chunk_ans = receive_Message(sock_alice)
					#TEST if the answer is not an error
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
						nb+=1
						break
				

				elif chunks_peers[i][1][j] == 'bob':
					send_Message(GET_CHUNK(chunk_hash),sock_bob)
					mess_chunk_ans = receive_Message(sock_bob)
					#TEST if the answer is not an error
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
						nb+=1
						break
				j+=1
		i+=1
	if nb == chunks_count:
		print("!!!! DOWNLOAD IS OVER !!!!\nReceived :",nb,' expected :',chunks_count) 
	else:
		print("Missing chunks, received :",nb,' expected :',chunks_count)
	sock_alice.close()
	sock_bob.close()
elif step == 2:
	# Step 2
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

		#Connect to the tracker
		sock_tracker.connect((IP_Tracker, PORT_Tracker))


		#BAD MESSAGE
		send_Message(Message(12),sock_tracker)
		print("Send request: NOTHING")

		mess_ans = receive_Message(sock_tracker)
		if message_format(mess_ans) == 3:
			print("The answer is a FILE_INFO\n")
			chunks_count,filename_length,filename,chunk_list= DECODE_FILE_INFO(mess_ans)
			print("\nchunks_count\n",chunks_count)
			print("\nfilename\n",filename)
			
		
			chunks_list,chunks_peers = make_standard(chunk_list,PORT_Alice,PORT_Bob)
		else:
			print("The answer is not a FILE_INFO")


		#GOOD MESSAGE 
		send_Message(GET_FILE_INFO(),sock_tracker)  
		print("Send request: GET_FILE_INFO")

		mess_ans = receive_Message(sock_tracker)
		if message_format(mess_ans) == 3:
			print("The answer is a FILE_INFO\n")
			chunks_count,filename_length,filename,chunk_list= DECODE_FILE_INFO(mess_ans)
			print("\nchunks_count\n",chunks_count)
			print("\nfilename\n",filename)
			
			
			chunks_list,chunks_peers = make_standard(chunk_list,PORT_Alice,PORT_Bob)
			ok = True
		else:
			print("The answer is not a FILE_INFO")
			ok = False



		if ok:
			sock_bob.connect((IP_Bob, PORT_Bob)) 
			sock_alice.connect((IP_Alice, PORT_Alice)) 
			#CODE CHARLIE STEP 1 = 2 with make_standard(chunk_list,PORT_Alice,PORT_Bob)

			i=0
			nb=0
			while i < chunks_count:
				#Define the chunk we want !
				chunk_hash = chunks_list[i][1]
				print("Send request for chunk: ",chunk_hash)
				if not isinstance(chunks_peers[i][1],tuple):
					#test if he is alone
					if chunks_peers[i][1] == 'alice':
						send_Message(GET_CHUNK(chunk_hash),sock_alice)
						mess_chunk_ans = receive_Message(sock_alice)
						#TEST if the answer is not an error
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
							nb+=1


					elif chunks_peers[i][1] == 'bob':
						send_Message(GET_CHUNK(chunk_hash),sock_bob)
						mess_chunk_ans = receive_Message(sock_bob)
						#TEST if the answer is not an error
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
							nb+=1

				elif isinstance(chunks_peers[i][1],tuple):
					j=0
					while j < len(chunks_peers[i][1]):

						if chunks_peers[i][1][j] == 'alice':
							send_Message(GET_CHUNK(chunk_hash),sock_alice)
							mess_chunk_ans = receive_Message(sock_alice)
							#TEST if the answer is not an error
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
								nb+=1
								break
						

						elif chunks_peers[i][1][j] == 'bob':
							send_Message(GET_CHUNK(chunk_hash),sock_bob)
							mess_chunk_ans = receive_Message(sock_bob)
							#TEST if the answer is not an error
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
								nb+=1
								break
							
						j+=1		
				i+=1

			if nb == chunks_count:
				print("!!!! DOWNLOAD IS OVER !!!!\nReceived :",nb,' expected :',chunks_count) 
			else:
				print("Missing chunks, received :",nb,' expected :',chunks_count)
		else:
			print("ERROR: IMPOSSIBLE TO READ MESSAGE BECAUSE IS NOT FILE_INFO ")
		sock_bob.close()
		sock_alice.close()
		sock_tracker.close()
		
elif step == 3:
	# Step 3
	path_chunks_charlie = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\chunks\\charlie')


	sock_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



	#Broadcast the tracker
	addr = ('255.255.255.255',9000)
	UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	print("Send discover tracker")
	UDPSock.sendto(Message_to_byte_array(DISCOVER_TRACKER()),addr)

	print("ANSWER :\n")

	ans = UDPSock.recvfrom(10000)
	print(ans)

	mess = byte_array_to_Message(ans[0])

	IP_Tracker,PORT_Tracker,tracker_name_length,tracker_name = DECODE_TRACKER_INFO(mess)
	print("ip_address",IP_Tracker)
	print("port_number",PORT_Tracker)
	print("tracker_name",tracker_name)


	print("Connexion tracker")
	sock_tracker.connect((IP_Tracker, PORT_Tracker))

	#BAD MESSAGE 
	send_Message(Message(12),sock_tracker)
	print("Send request: NOTHING")

	mess_ans = receive_Message(sock_tracker)
	if message_format(mess_ans) == 3:
		print("The answer is a FILE_INFO\n")
		chunks_count,filename_length,filename,chunk_list= DECODE_FILE_INFO(mess_ans)
		print("\nchunks_count\n",chunks_count)
		print("\nfilename\n",filename)
		
		chunks_list,chunks_peers = make_standard(chunk_list,PORT_Alice,PORT_Bob)
	else:
		print("The answer is not a FILE_INFO")


	#GOOD MESSAGE 
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



	print("================ Start to extract =================")
	#Create a list with all the ports, to create enough socket for each port
	i=0
	list_port = []
	list_index_tuple = []
	list_index_list = []

	while i <chunks_count:
		if  isinstance(chunks_list[i][1],tuple):
			list_index_tuple.append(i)   #One peer so we had it
			port = chunks_list[i][1][1] #Take the PORT
			ip = chunks_list[i][1][0] #Take the IP
			if port in list_port:
				pass
			else:
				list_port.append(port)

		elif isinstance(chunks_list[i][1],list):
			list_index_list.append(i)

			j=0
			while j < len(chunks_list[i][1]):
				port = chunks_list[i][1][j][1] #Take the port in the list
				ip = chunks_list[i][1][j][0] #Take the ip in the list
				if port in list_port:
					pass
				else:
					list_port.append(port)
				j+=1
		i+=1



	#We can fo through the list_index_tuple, et lis_index_list to do specific things

	nb_chunks =0
	for index in list_index_tuple:
		
		chunk_hash = chunks_list[index][0].decode("utf-8")
		ip = chunks_list[index][1][0] #take the ip
		port = chunks_list[index][1][1] #take the port
		sock_to_discuss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock_to_discuss.connect((ip, port))

		#We have the socket, the chunk and the ip
		send_Message(GET_CHUNK(chunk_hash),sock_to_discuss)
		mess_chunk_ans = receive_Message(sock_to_discuss)
		#TEST if the answer is not an error 
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

	print("!!!! DOWNLOAD TUPLE IS OVER !!!!")

	for index in list_index_list:
		
		chunk_hash = chunks_list[index][0].decode("utf-8")

		for element in chunks_list[index][1]:
			ip = element[0] #take the ip
			port = element[1] #take the port
			sock_to_discuss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			sock_to_discuss.connect((ip, port))

			#We have the socket, chunk and ip
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
				
				break
				

	print("!!!! DOWNLOAD LIST IS OVER !!!!")

	print("TOTAL CHUNK DOWNLOADED : " ,nb_chunks, "and the total of chunk was :", chunks_count, "Have all ?", nb_chunks==chunks_count)


elif step == 4:
	# Step !!BONUS!!
	path_chunks_charlie = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\chunks\\charlie')

	socket_bonus = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_bonus.connect(("164.15.76.104", 8000))


	mess=GET_FILE_INFO()
	send_Message(mess,socket_bonus)
	print("SEND GET_FILE_INFO")


	print("RECEIVE FILE")
	Message1 = receive_Message(socket_bonus)
	chunks_count,filename_length,filename,chunks_list = DECODE_FILE_INFO(Message1)
	print("\nChunks_count:\t",chunks_count)
	print("\nfilename_length:\t",filename_length)
	print("\nfilename:\t",filename)
	print("\nchunks_list:\t",chunks_list)


	print("================ Start to extract =================")
	#Create a list with all the ports, to create enough socket for each port
	i=0
	list_port = []
	list_index_tuple = []
	list_index_list = []

	while i <chunks_count:
		if  isinstance(chunks_list[i][1],tuple):
			list_index_tuple.append(i)   #One peer so we had it
			port = chunks_list[i][1][1] #take the port in the list
			ip = chunks_list[i][1][0] #take the ip in the list
			if port in list_port:
				pass
			else:
				list_port.append(port)

		elif isinstance(chunks_list[i][1],list):
			list_index_list.append(i)
			
			j=0
			while j < len(chunks_list[i][1]):
				port = chunks_list[i][1][j][1] #take the port in the list
				ip = chunks_list[i][1][j][0] #take the ip in the list
				if port in list_port:
					pass
				else:
					list_port.append(port)
				j+=1
		i+=1



	#We can fo through the list_index_tuple, et lis_index_list to do specific things
	nb_chunks =0
	for index in list_index_tuple:
		#print(index)
		chunk_hash = chunks_list[index][0].decode("utf-8")
		ip = chunks_list[index][1][0] #récuèpe l'ip
		port = chunks_list[index][1][1] #récuèpe le port
		sock_to_discuss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock_to_discuss.connect((ip, port))

		#We have the socket, ip, chunk
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

	print("!!!! DOWNLOAD TUPLE IS OVER !!!!")

	for index in list_index_list:
		
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
				break
				

	print("!!!! DOWNLOAD LIST IS OVER !!!!")

	print("TOTAL CHUNK DOWNLOADED : " ,nb_chunks, "and the total of chunk was :", chunks_count, "Have all ?", nb_chunks==chunks_count)




	#create file.ini to use merge chunks !! 

	print("CREATE FILE.INI")
	# lets create that config file
	cfgfile = open("../config/file.ini",'w')

	# add the settings to the structure of the file, and lets write it out...
	config = configparser.ConfigParser()
	config.add_section('description')
	config.set('description','filename',filename.decode("utf-8"))
	config.set('description','chunks_count',str(chunks_count))


	config.add_section('chunks')
	i=0
	while i<chunks_count:
		config.set('chunks',str(i),chunks_list[i][0].decode("utf-8"))
		i+=1

	config.write(cfgfile)
	cfgfile.close()
	print("FILE.INI CREATED")


else:
    print('Error: invalid step number')
    sys.exit(1)