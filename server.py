import socket
from _thread import *
import threading

print_lock = threading.Lock()

def threaded10(c):
     while True:
        try:
            data = c.recv(1024)
            dataStr = data.decode('utf-8')
            print(dataStr)
        except:
            print("Server Closed")
            c.close
            break


        requestMethod = dataStr.split(' ')[0]

        response = ""

        # extract file name from data stream DONE
        f = dataStr.split(' ',1)[1]
        fileName = f.split(' ',1)[0]
        fileName2 = fileName.split('/')[1]
        print('file name is',fileName2)
        if requestMethod == 'POST':
            # create file with this file name Done
            ff = open("server/fromClient/" + fileName2, "a+")
            # save payload in the file
            first = dataStr.split('\r\n\r\n')[1]
            ff.write(first + "\n")
            response = b"HTTP/1.0 200 Ok\r\nServer: Our server\r\n\r\n"
            print (response)
            c.sendall(response)

        elif requestMethod == 'GET':
            print("get request")
            # open file with this file name (try and catch) Done
            try:
                ext = fileName2.split(".")[1]

                if ext == "png":
                    fff = open("server/" + fileName2, "rb")
                    # print("server/" + fileName2)
                    stringResponse = fff.read()
                    msg = str(stringResponse)

                    # print(stringResponse)
                    response = "HTTP/1.1 200 OK\n " + "Server:Our server\r\n\r\n" + msg
                    print(response)
                    c.send(response.encode())

                else:
                    fff = open("server/" + fileName2, "r")
                    stringResponse = fff.read()
                    msg =  stringResponse
                    # print(stringResponse)
                    response = "HTTP/1.1 200 OK\n " + "Server:Our server\r\n\r\n" + msg
                    print(response)
                    c.send(response.encode())
            except:
                response = "HTTP/1.0 404 Not Found\n Server:Our server\r\n\r\n"
                c.send(response.encode())

        c.close()
     print_lock.release()


def threaded11(c):
    try:
        while True:
            t = 10
            y = 0
            try:
                data = c.recv(1024)
                dataStr = data.decode('utf-8')
            except :
                break

            requestMethod = dataStr.split(' ')[0]
            response = ""

            # extract file name from data stream DONE
            f = dataStr.split(' ', 1)[1]
            fileName = f.split(' ', 1)[0]
            fileName2 = fileName.split('/')[1]
            if requestMethod == 'POST':
                # create file with this file name Done
                ff = open("server/fromClient/" + fileName2, "a+")
                # save payload in the file
                first = dataStr.split('\r\n')[1]
                pload = first.split('?')[1]
                ff.write(pload + "\n")
                response = b"HTTP/1.1 200 Ok\r\nServer: Apache\r\n\r\n"
                c.sendall(response)

            elif requestMethod == 'GET':
                # open file with this file name (try and catch) Done
                try:
                    ext = fileName2.split(".")[1]
                    if ext == "png":
                        stringResponse = fff.read()
                        msg = str(stringResponse)

                        # print(stringResponse)
                        response = "HTTP/1.1 200 OK\n " + "Server:Our server\r\n\r\n" + msg
                        print(response)
                        c.send(response.encode())
                    else:
                        fff = open("server/" + fileName2, "r")
                        stringResponse = fff.read()
                        msg = fileName2 + "?" + stringResponse
                        # print(stringResponse)
                    response = "HTTP/1.1 200 OK\n " + "Server:Our server\r\n\r\n" + msg
                    c.send(response.encode())
                except:
                    # print("not found")
                    response = "HTTP/1.1 404 Not Found\n Server:Our server\r\n\r\n"
                    c.send(response.encode())
            print_lock.release()
            c.close()
    except:
        print("Server is Closing")


def Main():
    host = "127.0.0.1"
    port = 80
    choice = 1


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        print("socket binded to port", port)
        s.listen()
        print("socket is listening")
        while True:
            # establish connection with client
            c, addr = s.accept()

            # lock acquired by client
            print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            if choice == 1:
                start_new_thread(threaded10, (c,))
            else:
                s.settimeout(15)
                start_new_thread(threaded11, (c,))

    # s.close()


if __name__ == '__main__':
    Main()
