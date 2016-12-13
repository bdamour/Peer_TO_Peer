# coding: utf-8

import socket
from lib.Message import *
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

print("CREATION FILE.INI")
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
print("FIN CREATION FILE.INI")