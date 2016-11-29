#-*- coding :Latin -1 -*
import os
import struct
import glob

def encode(num, string):
	string = string.encode("utf-8")
	string_length = len(string)
	fmt = "!HB%ds" % string_length
	return struct.pack(fmt, num, string_length, string)

def decode(binary):
	fmt1 = "!HB"
	fmt1_size = struct.calcsize(fmt1)
	num, string_length = struct.unpack(fmt1, binary[:fmt1_size])
	fmt2 = "!%ds" % string_length
	(string,) = struct.unpack(fmt2, binary[fmt1_size:])
	return (num, string.decode("utf-8"))

num = 42
string = "Hello World!"
print("Original:\t", num, string)

binary = encode(num, string)
print("Encoded:\t", " ".join(map(hex, bytes(binary))))

new_num, new_string = decode(binary)
print("Decoded:\t", new_num, new_string)


#=======================================
path = glob.glob("*.bin")
print(path)
fichier = open(path[0],"rb")
size = os.path.getsize(path[0])
print(size // 1024)
for i in range(size // 1024):
	print(i)

#fichier.close()

os.system("pause")