'''
SDN-based-QoS-Enhanced-Virtualization-in-Service-Provider-Networks
EE-297B project, code by Sohail Virani, Goutham Prasanna, Nitish Gupta. 

'''
#CDN client requesting content from the CDN server
import socket
import sys

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8080)
print >>sys.stderr, 'connecting to %s port %s' % server_address
s.connect(server_address)
try:
    
    # Send data
    message = 'user1 pass1 sjsutour.mp4'
    print >>sys.stderr, 'sending "%s"' % message
    s.sendall(message)
    data = s.recv(1024)

    host,port,content_id,filesize = data.split(" ")
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
    s.connect((host,int(port)))
    s.sendall("%s %s" %(content_id,filesize))

    # Look for the response
    
    amount_expected = int(filesize)
    with open("sjsutour.mp4","wb") as f:
	
    	while amount_received < amount_expected:
    	    data = s.recv(2048)
	    f.write(data)
    	    amount_received += len(data)

    	    #print >>sys.stderr, 'received "%s"' % data
    
finally:	
    				
    print >>sys.stderr, 'closing socket'
    s.close()
