import socket,pickle
import threading
import os

def retriveFile(name, sok):
    useresponse = sok.recv(1024)
    fl = []
    for dirpath, dirnames, filenames in os.walk('./'):
        fl.extend(filenames)
    bytesToSend = pickle.dumps(fl)
    if useresponse[:2] == "OK":
        sok.send(bytesToSend)
    filename = sok.recv(1024)
    if os.path.isfile(filename):
        sok.send("Exists " + str(os.path.getsize(filename)))
        useresponse = sok.recv(1024)
        if useresponse[:2] == "OK":
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sok.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sok.send(bytesToSend)
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
