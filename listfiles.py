import os,pickle,socket,threading

host='127.0.0.1'
port=5666
s=socket.socket()
s.bind((host,port))
s.listen(5)
print "server running"
conn,addr=s.accept()
print "connected on addr",addr
useresponse = conn.recv(1024)
fl=[]
for dirpath,dirnames,filenames in os.walk('./'):
    fl.extend(filenames)
bytesToSend = pickle.dumps(fl)
if useresponse[:2]=="OK":
        conn.send(bytesToSend)
conn.close()

