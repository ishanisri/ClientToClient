# Python program to implement server side.
import socket
import select
import sys
from _thread import *

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])

print("Server started ...")

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []
destination_address = 0 #default
msg_buffer = ""

def clientthread(conn, addr):

	# sends a message to the client whose user object is conn
	pos = len(list_of_clients)
	if(pos-1) == 0:
		print(str(conn.getpeername()) + " connected as A")
		message_first = "You are connected as A"
	elif(pos -1) == 1:
		print(str(conn.getpeername()) + " connected as C")
		message_first = "You are connected as C"
	elif(pos -1) == 2:
		print(str(conn.getpeername()) + " connected as D")
		message_first = "You are connected as D"


	conn.send(message_first.encode())

	while True:
			try:
				message = conn.recv(1030).decode()

				if message:
					destination_addr = message[0]
					# get the destination client number
					msg =message[1:]
					if (msg.lower() == "exit"):
						# shut down the thread in case of exit.
						last_msg = "Closing down"
						conn.send(last_msg.encode())
						conn.close()
						remove(conn)

					else:
						if(msg[:4] == "file:"):
							# check if file is being forwarded
							dest_file = message[0]
							msg_info = msg[5:]
							message_to_send = "<" + str(conn.getpeername()) + "> " + msg_info
							routing(message_to_send, conn,dest_file,addr)


						elif(len(message) != 1 ):
							"""prints the message and address of the
							user who just sent the message on the server
							terminal"""
							print ("<" + str(conn.getpeername()) + "> " + msg)
							# Calls routing function to forward the message
							message_to_send = "<" + str(conn.getpeername()) + "> " + msg
							routing(message_to_send, conn,destination_addr,addr)
						else:
							pass


				else:
					"""message may have no content if the connection
					is broken, in this case we remove the connection"""
					remove(conn)

			except:
				continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def routing(message, conn, destination_addr, addr):
	dest = int(destination_addr)
	connection = list_of_clients[dest]


	for clients in list_of_clients:
		if clients == connection:
			try:
				clients.send(message.encode())
				print("Sent to the client")
			except:
				clients.close()
				# if the link is broken, we remove the client
				remove(clients)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:

	"""Accepts a connection request and stores two parameters,
	conn which is a socket object for that user, and addr
	which contains the IP address of the client that just
	connected"""
	conn, addr = server.accept()

	"""Maintains a list of clients for ease of broadcasting
	a message to all available people in the chatroom"""
	list_of_clients.append(conn)

	# prints the address of the user that just connected


	# creates and individual thread for every user
	# that connects
	start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
