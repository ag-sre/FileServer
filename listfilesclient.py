import os,pickle,socket,threading

host='127.0.0.1'
port=5666
s=socket.socket()
s.connect((host,port))
message=raw_input("Do you want to download files(y/n)?")
if message=='y':
    s.send("OK")
    data=s.recv(4096)
    d_arr=pickle.loads(data)
    print d_arr
else:
    print "exiting"

