import socket

HOST = ''   
PORT = 9999 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
fd = open("sample.txt","w")
conn, addr = s.accept()
while 1:        
        data = conn.recv(1024)
        if not data: break
        fd.write(data + "\n")
fd.close()
#conn.close()
s.close()
