import socket,pickle
import threading
import os

def retriveFile(name, sok):
    useresponse="01"
    while useresponse!="05":
        print "testloop"
        useresponse = sok.recv(1024)
        print (useresponse[:2])
        fl = []
        for dirpath, dirnames, filenames in os.walk('./'):
            fl.extend(filenames)
        bytesToSend = pickle.dumps(fl)
        print "test"
        if useresponse[:2] == "01":
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
        elif useresponse[:2] == "02":
            sok.sendall("OK".encode('utf-8'))
            filename = sok.recv(1024).decode('utf-8')
            print(filename)
            uploadfile = filename
            if os.path.isfile(uploadfile):
                print("File already exists in Server")
                sok.send("ERR")
            else:
                with open(uploadfile, 'wb') as file_to_write:
                    while True:
                        data = sok.recv(1024)
                        print(data)
                        if not data:
                            break
                        file_to_write.write(data)
                    print("File Uploaded")
        elif useresponse[:2] == "03":
            print "test2"
            sok.send(bytesToSend)
            filename = sok.recv(1024)
            if os.path.isfile(filename):
                sok.send("Exists " + str(os.path.getsize(filename)))
                newname = sok.recv(1024)
                os.rename(filename,newname)
                sok.send("Success")
                newf=[]
                for dirpath, dirnames, nfilenames in os.walk('./'):
                    newf.extend(nfilenames)
                newFileList = pickle.dumps(newf)
                sok.send(newFileList)
            else:
                sok.send("ERR")
        elif useresponse[:2] == "04":
            sok.sendall("OK".encode('utf-8'))
            fl = []
            for dirpath, dirnames, filenames in os.walk('./'):
                fl.extend(filenames)
            filesToSend=pickle.dumps(fl)
            sok.send(filesToSend)
            filename = sok.recv(1024)
            print(filename)
            if os.path.isfile(filename):
                os.remove(filename)
                print("File removed successfully!")
                sok.send("Deleted")
            else:
                print("File not found in Server!")
                sok.send("ERR")
    sok.close()

def Main():
    host = '127.0.0.1'
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print "Server started"

    c, addr = s.accept()
    print "client connected to ip:<", str(addr), ">"
    t = threading.Thread(target=retriveFile, args=("retrThread", c))
    t.start()


if __name__ == '__main__':
    Main()
