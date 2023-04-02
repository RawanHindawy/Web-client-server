# Import socket module
import socket
from PIL import Image

cache = []
cacheCount = 0

def readFile():
    lines = []
    with open('client/requests.txt', 'r') as f:
        lines = f.readlines()
        lent = len(lines)
        method = [None] * lent
        port = [None] * lent
        host = [None] * lent
        headers = [None] * lent
        hostPort = [None] * lent
    count = 0
    for line in lines:

        line = line.replace("\n", "")
        print(f'line {count+1}: {line}')
        method[count], headers[count], hostPort[count] = line.split(' ', 2)

        try:
            host[count],port[count] = hostPort[count].split(' ', 1)
            port[count] = int(port[count])

        except:
            host[count] = hostPort[count]
            port[count] = 80
        count += 1

    return method,headers, host, port

def add_cach(request,response):
    global cacheCount
    first = response.split(' ')[1]
    code = first.split(' ')[0]
    method = request.split(" ")[0]
    ch = {'request':request,
          'method':method,
          'response': response,
          'code':code}
    cache.append(ch)
    cacheCount += 1

def is_cached(request):
    for item in cache:
        if request in item['request']:
            # index = item['request'].index(request)
            # reques = item['request'][index].split(" ")[0]
            if item['method'] == "POST" or item['code'] == '404':
                ret = {"message":item['response'], "status":"res" }
                return ret
            else:
                ret = {"message": item['request'], "status": "found"}
                return ret
    return False

def Main():

    method, headers, host, port = readFile()
    choice = 1
    for x in range(len(method)):
        if choice == 2:
            request1 = " HTTP/1.1\nHost : "
        else:
            request1 = " HTTP/1.0\nHost : "
        request2 = method[x] + " "
        request3 = host[x] + " "
        request4 = str(port[x])
        request5 = "/" + headers[x]
        req = ""
        # msg = "%s %s HTTP/1.0\r\nHost:%s %s" %method[x], headers[x],
        if method[x] == 'GET':
            req = request2 + request5 + request1 + str(request3) + str(request4) + "\r\n"

        elif method[x] == 'POST':
            file = "client/" + headers[x]
            f = open(file, "r")
            pload = headers[x] + "?" + f.read()
            req = request2 + request5 + request1 + str(request3) + str(request4) + "\r\n\r\n" + pload

        message = req
        if cacheCount > 0:
            ok = is_cached(message)
            if ok:
                if ok['status'] == "found":
                    print("the file was found before: %s was found" % ok['message'])
                    f = ok['message'].split(' ', 1)[1]
                    fileName = f.split(' ', 1)[0]
                    fileName2 = fileName.split('/')[1]
                    file = "client/fromServer/" + fileName2
                    f = open(file, "r")
                    print(f.read())
                    print("\n")
                    continue
                else:
                    print("the file request was served before: %s was the response" % ok['message'])
                    continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect_ex((host[x],int(port[x])))
            # message sent to server
            s.sendall(bytes(message,'utf-8'))

            while True:
                try:
                    headers[x]=headers[x].split("/",1)[1]
                except:
                    break
            print("Sent")


            data = s.recv(1024)
            dataa = str(data.decode('utf-8'))
            if method[x] == 'GET':
                notFound = 0
                cod = dataa.split(' ')[1]
                cod = cod.split(' ')[0]
                if cod == "404":
                    notFound = 1
                if notFound == 0:
                    # message received from server
                    dataa = dataa.split("\r\n\r\n")[1]
                    fil = "client/fromServer/" + headers[x]
                    #fil = headers[x]

                    ext = fil.split(".")[1]
                    if ext == "html":
                        f = open(fil, "w")
                        add_cach(message, dataa)
                        f.write(dataa + "\n")

                    elif ext == "png":
                        f = open(fil, "wb")
                        add_cach(message, dataa)
                        # f.write(dataa)
                        f.write(bytes(8))  # write 8 null bytes to the file
                        f.write(dataa.encode())
                        # img =Image.open(fil)
                        # img.show()
                        print("opening png")
                    else:
                        f = open(fil, "a+")
                        add_cach(message, dataa)
                        print(dataa)
                        f.write(dataa + "\n")
                        print('Received from the server :', str(data.decode('utf-8')))
                else:
                    print(dataa)
            else:
                add_cach(message, dataa)
                print('Received from the server :', str(data.decode('utf-8')))
    s.close()


if __name__ == '__main__':
    Main()
