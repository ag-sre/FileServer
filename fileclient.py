import os
import socket,pickle
def Download(s):
    s.send("01")
    data = s.recv(4096)
    d_arr = pickle.loads(data)
    print d_arr
    filename=raw_input("Filename? ->\n")
    if filename!='q':
        s.send(filename)
        data=s.recv(1024)
        if data[:6] == 'Exists':
            filesize=long(data[6:])
            message=raw_input("File Exists,"+str(filesize)+"bytes (y/n)?\n")
            if message =='y':
                s.send('OK')
                f=open('client/new_'+filename,'wb')
                data=s.recv(1024)
                totalRecv=len(data)
                f.write(data)
                while totalRecv< filesize:
                    data=s.recv(1024)
                    totalRecv+=len(data)
                    f.write(data)
                    print "{0:2f)".format((totalRecv/float(filesize))*100)+"% Done"
                print "Download Complete!"
        else:
            print "File does not exist"
    s.close()

def Rename(s):
    s.send("03")
    data = s.recv(4096)
    d_arr = pickle.loads(data)
    print d_arr
    filename = raw_input("enter file to rename?(q to quit) ->\n")
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'Exists':
            filesize = long(data[6:])
            message = raw_input("File Exists," + str(filesize) + "bytes"+"\nEnter new name->")
            s.send(message)
            data = s.recv(1024)
            if data=="Success":
                print "Renamed successfully!"
                newFileList=s.recv(4096)
                newFileList=pickle.loads(newFileList)
                print "Files on server:\n",newFileList
        else:
            print "File does not exist"
    else:
        return


def Upload(s):
    s.send("02")
    ack = s.recv(1024)
    if (ack.decode('utf-8') == "OK"):
        file = raw_input("enter file to upload?(q to quit) ->\n")
        if file != 'q':
            file = file.split('\n')
            fl = []
            for dirpath, dirnames, filenames in os.walk('./client'):
                fl.extend(filenames)
            print (file[0])
            if file[0] in fl:
                print("File present in system")
                s.sendall(file[0].encode('utf-8'))
                if(s.recv(1024) == "ERR"):
                    print("File already exists in Server!!")
                else:
                    with open('client/'+file[0], 'rb') as file_to_send:
                        for data in file_to_send:
                            s.sendall(data)
                    print('end')
                    print("Upload Complete!")
    else:
        print ("Connection Error!")

def Delete(s):
    s.send("04")
    ack = s.recv(1024)
    if (ack.decode('utf-8') == "OK"):
        file = raw_input("enter file to delete?(q to quit) ->\n")
        if file != 'q':
            file = file.split('\n')
            fl = []
            for dirpath, dirnames, filenames in os.walk('./server'):
                fl.extend(filenames)
            print (file[0])
            if file[0] in fl:
                print("File present in system")
                s.sendall(file[0].encode('utf-8'))
                if (s.recv(1024) == "ERR"):
                    print("File doesnt exists in Server!!")
                else:
                    print('end')
                    print("Delete Complete!")
    else:
        print ("Connection Error!")
    s.close()

def Main():
    host='127.0.0.1'
    port=5000
    s=socket.socket()
    s.connect((host,port))
    message = raw_input("Select your option:\n1. Download\n2. Upload\n3. Rename\n4.Delete)?")
    if message=='1':
        Download(s)
    elif message=='2':
        Upload(s)
    elif message=='3':
        Rename(s)
    elif message=='4':
        Delete(s)
if __name__=='__main__':
    Main()