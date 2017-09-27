import socket,pickle
import threading
import os

def retriveFile(name, sok):
    useresponse = sok.recv(1024)
    print useresponse
    fl = []
    for dirpath, dirnames, filenames in os.walk('./server'):
        fl.extend(filenames)
    bytesToSend = pickle.dumps(fl)
    print "test"
    if useresponse[:2] == "01":
        sok.send(bytesToSend)
        filename = sok.recv(1024)
        if os.path.isfile('server/'+filename):
            sok.send("Exists " + str(os.path.getsize('server/'+filename)))
            useresponse = sok.recv(1024)
            if useresponse[:2] == "OK":
                with open('server/'+filename, 'rb') as f:
                    bytesToSend = f.read(1024)
                    sok.send(bytesToSend)
                    while bytesToSend != "":
                        bytesToSend = f.read(1024)
                        sok.send(bytesToSend)
        else:
            sok.send("ERR")
    elif useresponse[:2] == "03":
        print "test2"
        sok.send(bytesToSend)
        filename = sok.recv(1024)
        if os.path.isfile('server/' + filename):
            sok.send("Exists " + str(os.path.getsize('server/' + filename)))
            newname = sok.recv(1024)
            os.rename('server/'+filename,'server/'+newname)
            sok.send("Success")
            newf=[]
            for dirpath, dirnames, nfilenames in os.walk('./server'):
                newf.extend(nfilenames)
            newFileList = pickle.dumps(newf)
            sok.send(newFileList)
        else:
            sok.send("ERR")
    sok.close()

def Main():
    host = '127.0.0.1'
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print "Server started"
    while True:
        c, addr = s.accept()
        print "client connected to ip:<", str(addr), ">"
        t = threading.Thread(target=retriveFile, args=("retrThread", c))
        t.start()
    s.close()


if __name__ == '__main__':
    Main()
