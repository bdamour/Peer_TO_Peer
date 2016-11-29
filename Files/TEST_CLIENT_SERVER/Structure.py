#-*- coding :Latin -1 -*
import os
import struct
import glob
import sys

def encode_header(version, msg_type,msg_length):
	fmt = "!BB2xI"
	return struct.pack(fmt, version,msg_type,msg_length)

def decode_header(binary):
	fmt1 = "!BB2xI"
	version, msg_type,msg_length = struct.unpack(fmt1, binary)
	return (version, msg_type,msg_length)

def encode_error(error_code):
	fmt = "!H2x"
	return struct.pack(fmt, error_code)

def encode_filename(filename):
	filename = filename.encode("utf-8")
	lentgh_filename = len(filename)
	lentgh = lentgh_filename
	reste = lentgh%4
	if reste==0:
		lentgh += lentgh//4
	else:
		lentgh += reste
	fmt = "!H%ds2x" % lentgh
	return struct.pack(fmt,lentgh_filename, filename)

def decode_filename(binary):
	fmt1 = "!H"
	fmt1_size = struct.calcsize(fmt1)
	(filename_size,) =struct.unpack(fmt1, binary[:fmt1_size])

	fmt2 = "!%ds" % filename_size
	fmt2_size = struct.calcsize(fmt2)

	(filename,) = struct.unpack(fmt2, binary[fmt1_size:fmt2_size+fmt1_size])
	return (filename_size,filename.decode("utf-8"))


filename = "Bonjour toi petit escargot!"
binary0 = encode_filename(filename)
print(len(filename))
print("Encoded:\t", " ".join(map(hex, bytes(binary0))))
filesize,filename0 = decode_filename(binary0)
print("Decoded:\t",filesize,filename0 )

"""
version = 1
msg_type = 2
msg_length = 1024
print("Original:\t", version, msg_type,msg_length)
binary = encode_header(version, msg_type,msg_length)

print(binary[0:8]) #Selectionne les 8 premiers bites

print("Encoded:\t", " ".join(map(hex, bytes(binary))))

version2, msg_type2,msg_length2 = decode_header(binary)
print("Decoded:\t", version2, msg_type2,msg_length2)



# DISCOVER_TRACKER
DISCOVER_TRACKER = encode_header(1,0,2)

#GET_FILE_INFO
GET_FILE_INFO = encode_header(1,2,2)


#================ DECODE ENCODE CHUNCK_HASH 20 bytes ==============
def encode(string):
	string = string.encode("utf-8")
	string_length = len(string)
	fmt = "!20s" 
	return struct.pack(fmt,string)

def decode(binary):
	fmt2 = "!20s" 
	(string,) = struct.unpack(fmt2, binary)
	return string.decode("utf-8")


s = "7890e131622631d2e09e55a74ec7a1aab75d6330"
print("Original:\t", s)
binary0 = encode(s)
print("Encoded:\t", " ".join(map(hex, bytes(binary0))))
new_s = decode(binary0)
print("Decoded:\t", new_s)
"""

"""
#=======================================
path = glob.glob("*.bin")
print(path)
fichier = open(path[0],"rb")
size = os.path.getsize(path[0])
print(size // 1024)
for i in range(size // 1024):
	print(i)

#fichier.close()


os.system("pause")"""