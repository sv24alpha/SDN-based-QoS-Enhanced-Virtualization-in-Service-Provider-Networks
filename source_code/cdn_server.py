import time, os, sys, string, threading, math
'''
SDN-based-QoS-Enhanced-Virtualization-in-Service-Provider-Networks
EE-297B project, code by Sohail Virani, Goutham Prasanna, Nitish Gupta. 

'''
#Code for CDN Authentication and content fetch server
from socket import * 
class Server():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		 #Creating socket object
		self.serv = socket(AF_INET,SOCK_STREAM)

	    	#bind socket to address
		self.serv.bind((self.host, self.port))
		self.serv.listen(5) #Setting up the max number of connections we allow as 5 just for testing
		print 'Server up and running! Listening for incomming connections...'
		self.database ={"sjsutour.mp4":["c1.mp4",13070749]}
		self.server_info = {"cdn1":["localhost",20000],"cdn2":["localhost",30000]}
	def acceptConnections(self):
		conn, addr = self.serv.accept() ## accept incoming connection
		data = conn.recv(1024)
		
		print 'Connected by ', addr
		print "Message From " + addr[0] + " : " + data
		
		print ">>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<"
		username,password,filename = data.split(" ") #Customer authentication and media fetch
		content_id,filesize = self.database[filename]
		host,port = self.server_info["cdn1"]

		data = "%s %s %s %s" %(host,port,content_id,filesize) #Sending media server details back to client
		conn.send(data)
		print data

##Setting up variables
HOST = 'localhost'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 2048

if __name__ == '__main__':
  webServer = Server(HOST, PORT)

 

  while 1:
    webServer.acceptConnections()

#conn.close()

