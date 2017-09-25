import socket,pickle
def Main():
    host='127.0.0.1'
    port=5000
    s=socket.socket()
    s.connect((host,port))
    message = raw_input("Do you want to download files(y/n)?")
    if message == 'y':
        s.send("OK")
        data = s.recv(4096)
        d_arr = pickle.loads(data)
        print d_arr
    filename=raw_input("Filename? ->")
    if filename!='q':
        s.send(filename)
        data=s.recv(1024)
        if data[:6] == 'Exists':
            filesize=long(data[6:])
            message=raw_input("File Exists,"+str(filesize)+"bytes (Y/N)?")
            if message =='Y':
                s.send('OK')
                f=open('new_'+filename,'wb')
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
if __name__=='__main__':
    Main()