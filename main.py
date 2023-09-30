import socket

IP = "127.0.0.1"
PORT = 8080
STATUS_200 = "HTTP/1.0 200 OK\r\n"
STATUS_301 = "HTTP/1.0 301 Moved Permanently\r\n"
STATUS_404 = "HTTP/1.0 404 Not Found\r\n"

# Creates and sends the 404 response
def send_404_page(connection):
    with open('404_page.html', "rb") as file:
        data = file.read()
    response_code = STATUS_404
    response_code += "Content-Type: text/html\r\n"
    response_code += "Content-Length: {}\r\n\r\n".format(len(data))
    response_code = response_code.encode("utf-8") + data
    connection.send(response_code)

# Starts the server and connection
def server():
    # Create a TCP/IP socket, AF_INET for IPv4 address protocol, SOCK_STREAM for socket type
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    clientSocket.bind((IP, PORT))
    clientSocket.listen(1)

    print("Waiting for a connection...")

    while True:
        connection, client_address = clientSocket.accept()
        print("Connection Accepted")
        request = connection.recv(1024)
        # print(request)

        request_get_line = request.decode("utf-8").split("\r\n")
        # print(request_get_line)
        first_line = request_get_line[0]
        # print(first_line)
        parts = first_line.split(" ")

        requested_file = ""

        if len(parts) >= 2:
            # print(parts)
            requested_file = parts[1]
            requested_file = requested_file[1:]

        if requested_file == "page1.html":
            # Send the data to the client
            response_code = STATUS_301
            response_code += "Location: /page2.html\r\n"
            response_code = response_code.encode("utf-8")
            connection.send(response_code)
        elif '.html' in requested_file:
            try:
                with open(requested_file, "rb") as file:
                    data = file.read()
                    print("File opened")
                # Send the data to the client
                response_code = STATUS_200
                response_code += "Content-Type: text/html\r\n"
                response_code += "Content-Length: {}\r\n\r\n".format(len(data))
                response_code = response_code.encode("utf-8") + data
                connection.send(response_code)
            except FileNotFoundError:
                # Send the data to the client
                send_404_page(connection)
        elif '.jpg' in requested_file:
            try:
                with open(requested_file, "rb") as file:
                    data = file.read()
                    print("File opened")
                    # Send the data to the client
                response_code = STATUS_200
                response_code += "Content-Type: image/jpg\r\n"
                response_code += "Content-Length: {}\r\n\r\n".format(len(data))
                response_code = response_code.encode("utf-8") + data
                connection.send(response_code)
            except FileNotFoundError:
                # Send the data to the client
                send_404_page(connection)
        connection.close()


server()
