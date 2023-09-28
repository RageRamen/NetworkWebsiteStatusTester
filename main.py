import socket

IP = "127.0.0.1"
PORT = 8080
STATUS_200 = "HTTP/1.0 200 OK\r\n"
STATUS_301 = "HTTP/1.0 301 Moved Permanently\r\n"
STATUS_404 = "HTTP/1.0 404 Not Found\r\n"

# Create a TCP/IP socket, AF_INET for IPv4 address protocol, SOCK_STREAM for socket type
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server.bind((IP, PORT))
server.listen(1)

print("Waiting for a connection...")

while True:
    connection, client_address = server.accept()
    print("Connection Accepted")
    request = connection.recv(1024)
    # print(request)

    request_get_line = request.decode("utf-8").split("\r\n")
    # print(request_get_line)
    first_line = request_get_line[0]
    # print(first_line)
    parts = first_line.split(" ")
    # print(parts)

    if len(parts) >= 2:
        requested_file = parts[1]
        if requested_file == "/index.html":
            try:
                with open("index.html", "rb") as file:
                    data = file.read()
                    print("File opened")
                    # Send the data to the client
                response = STATUS_200 + data.decode("utf-8")
                response += "Content-Type: text/html\r\n"
                response += "Content-Length: {}\r\n\r\n".format(len(data))
                response = response.encode("utf-8") + data
                connection.send(response)
            except FileNotFoundError:
                # Send the data to the client
                response_code = "HTTP/1.0 404 Not Found\r\n"
                response_code += "Content-Type: text/html\r\n\r\n"
                response_code += "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
                connection.send(response_code.encode('utf-8'))
        elif requested_file == "/Ramen.jpg":
            try:
                with open("Ramen.jpg", "rb") as file:
                    data = file.read()
                    print("File opened")
                    # Send the data to the client
                response = STATUS_200
                response += "Content-Type: image/jpg\r\n"
                response += "Content-Length: {}\r\n\r\n".format(len(data))
                response = response.encode("utf-8") + data
                connection.send(response)
            except FileNotFoundError:
                # Send the data to the client
                response_code = "HTTP/1.0 404 Not Found\r\n"
                response_code += "Content-Type: text/html\r\n\r\n"
                response_code += "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
                connection.send(response_code.encode('utf-8'))
        elif requested_file == "/page1.html":
            # Send the data to the client
            response = STATUS_301
            response += "Location: /page2.html\r\n"
            response = response.encode("utf-8")
            connection.send(response)
        elif requested_file == "/page2.html":
            try:
                with open("page2.html", "rb") as file:
                    data = file.read()
                    print("File opened")
                    # Send the data to the client
                response = STATUS_200 + data.decode("utf-8")
                response += "Content-Type: text/html\r\n"
                response += "Content-Length: {}\r\n\r\n".format(len(data))
                response = response.encode("utf-8") + data
                connection.send(response)
            except FileNotFoundError:
                # Send the data to the client
                response_code = "HTTP/1.0 404 Not Found\r\n"
                response_code += "Content-Type: text/html\r\n\r\n"
                response_code += "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
                connection.send(response_code.encode('utf-8'))
        else:
            try:
                with open(requested_file, "rb") as file:
                    data = file.read()
                    print("File opened")
                    # Send the data to the client
                response = STATUS_200 + data.decode("utf-8")
                response += "Content-Type: text/html\r\n"
                response += "Content-Length: {}\r\n\r\n".format(len(data))
                response = response.encode("utf-8") + data
                connection.send(response)
            except FileNotFoundError:
                # Send the data to the client
                response_code = "HTTP/1.0 404 Not Found\r\n"
                response_code += "Content-Type: text/html\r\n\r\n"
                response_code += "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
                connection.send(response_code.encode('utf-8'))
    connection.close()
