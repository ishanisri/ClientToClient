# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:

	# maintains a list of possible input streams
	sockets_list = [sys.stdin, server]

	""" There are two possible input situations. Either the
	user wants to give manual input to send to other people,
	or the server is sending a message to be printed on the
	screen. Select returns from sockets_list, the stream that
	is reader for input. So for example, if the server wants
	to send a message, then the if condition will hold true
	below.If the user wants to send a message, the else
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			print("")
			message = socks.recv(1047).decode()
			if(message == "Closing down"):
				print(message)
				sys.exit()
			else:
				print(message)
				if("file:" in message):
					msg_to_write = message[int(message.find("file")):]
					print("Writing in file....")
					file = open("copied_file.txt",'a+')
					file.write(msg_to_write)
					file.close()
		else:
			start_text = sys.stdin.readline()
			msg_type = input("Enter 1 for file and 2 for text")

			if(str(msg_type) =='1'):
				filename = input("Enter filename:")
				dest = input("Destination:")
				file = open(filename,'rb')
				line = file.read(1024)
				dest_line = str(dest)+"file:"
				server.send(dest_line.encode())
				while (line):
					final_line = dest_line + line.decode('utf-8')
					server.send(final_line.encode())

					print('Sent ',final_line)
					#server.send(dest_line.encode())
					line = file.read(1024)
				server.send(str(dest_line +("end")).encode())
				file.close()


			else:
				message = input("Enter text:")
				dest = input("Destination:")
				dest_line = str(dest)
				final_msg = str(dest) + message
				server.send(final_msg.encode())
				sys.stdout.write("<You>")
				sys.stdout.write(message)
				sys.stdout.write("\n")
				sys.stdout.flush()


server.close()
