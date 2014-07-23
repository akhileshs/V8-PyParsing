import socket, sys

def sender(inputfile):
    HOST = "127.0.0.1" 
    PORT = 9999             
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    fd = open(inputfile,"r")
    print "Transmitting data from: ",inputfile," to: ",HOST
    while 1:        
        sendMsg = fd.readline()
        if not sendMsg:
            break
        s.send(sendMsg)
    s.close()

if __name__ == "__main__":
    sender(sys.argv[1])


