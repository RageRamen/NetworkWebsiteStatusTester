# Name: Bryan Ho
# UTA ID: 1001705601

import socket
import threading

# IP address is our localhost or 127.0.0.1 and will be used in the browser
IP = "127.0.0.1"
# Port number is 8080 and will be used in the browser
PORT = 8080
# Status codes for each connection and should be added to each response
# This is the status code for 200 OK
STATUS_200 = "HTTP/1.0 200 OK\r\n"
# This is the status code for 301 Moved Permanently for the page1 to page2
STATUS_301 = "HTTP/1.0 301 Moved Permanently\r\n"
# This is the status code for 404 Not Found which should display a custom 404 page after
STATUS_404 = "HTTP/1.0 404 Not Found\r\n"


####################################
# Input: connection
# Output: None
# Purpose: handles the connection from the clients, creates and sends the appropriate 200, 301, or 404 response
####################################
def client_thread(connection):
    # Used https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/ as reference
    # for helping me figure out the parts of the request line and how to obtain the requested file in the get line

    # Also used https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
    # as reference for how to create the response_code and what to add in it like the status codes, content type, content
    # length, and the data of the html pages.

    # Gets the request line from the browser with contains the get line
    request = connection.recv(1024)
    # print(request)  # Uncomment this line to see the request line

    # Gets the request line as an array of strings, mainly to get the get line easier in position 0
    request_array = request.decode("utf-8").split("\r\n")
    # print(request_array) # Uncomment this line to see the request line as an array of strings

    # Gets the first line of the request array which is actually the get line containing the requested file like GET /index.html HTTP/1.1
    get_line = request_array[0]
    # print(get_line) # Uncomment this line to see the get line

    # Gets the get line as an array of strings separated by the spaces, should look like [GET, /index.html, HTTP/1.1]
    get_line_array = get_line.split(" ")
    # print(get_line_array)

    # Checks if the get_line is the right length and is a get request since at position 1 is the requested file
    if len(get_line_array) >= 2:
        # Gets the requested file from the get_line array at position 1
        requested_file = get_line_array[1]
        # removed the "/" in the first character location since the requested file is in the same directory as the source code
        requested_file = requested_file[1:]

        # Checks firstly if requested file is page1.html, must return response of 301 to redirect to page2.html
        if requested_file == "page1.html":
            # Opens page2.html since page1.html was the requested file, but was relocated in this case
            with open("page2.html", "rb") as file:
                # Stores the data of the requested file page2.html
                data = file.read()
                # Prints that the page2.html was opened successfully
                print("File opened: page2.html")
            # Sets response as the 301 status code for page1.html
            response_code = STATUS_301
            # Adds that the location is at page2.html so that it can redirect from page1 to page2
            response_code += "Location: /page2.html\r\n"
            # Adds that the content type is html text for page2.html
            response_code += "Content-Type: text/html\r\n"
            # Adds what the content length of the html text file is, which is page2.html's length in bytes
            response_code += "Content-Length: {}\r\n\r\n".format(len(data))
            # Encodes the response in standard utf-8 and adds the page2.html data
            response_code = response_code.encode("utf-8") + data
            # Sends the response to the connection as a 301 status code which should redirect to page2.html
            # and separately request page2's data in another get line
            connection.send(response_code)

        # Checks if the requested file is any other html file
        elif '.html' in requested_file:
            try:
                # Tries to open the requested file at the same directory as the source code
                with open(requested_file, "rb") as file:
                    # Stores the data of the requested file
                    data = file.read()
                    # prints that the file was opened successfully
                    print("File opened: " + requested_file)
                # Sets the response to the 200 status code for a successful request
                response_code = STATUS_200
                # Adds that the content type is html text
                response_code += "Content-Type: text/html\r\n"
                # Adds what the content length of the html text file is
                response_code += "Content-Length: {}\r\n\r\n".format(len(data))
                # Encodes the response in standard utf-8 and adds the data of the html text file
                response_code = response_code.encode("utf-8") + data
                # Sends the 200 response to the connection to display the html page
                connection.send(response_code)
            # If the opening of the requested file was unsuccessful, it means that the file was not found and so a 404 response is issued
            except FileNotFoundError:
                # Runs the send_404_page method to send the appropriate 404 response to the connection
                send_404_page(connection)
        # Checks if the requested file is a .jpg file in order to correctly display jpg images into the html pages
        elif '.jpg' in requested_file:
            try:
                # Tries to open the requested image at the same directory as the source code
                with open(requested_file, "rb") as file:
                    # Stores the data of the requested image
                    data = file.read()
                    # Prints that the image was opened successfully
                    print("Image opened: " + requested_file)
                # Sets the response to the 200 status code for a successful request
                response_code = STATUS_200
                # Adds that the content type is image jpg file
                response_code += "Content-Type: image/jpg\r\n"
                # Adds what the content length of the image jpg file is, normally in bytes
                response_code += "Content-Length: {}\r\n\r\n".format(len(data))
                # Encodes the response in standard utf-8 and adds the data of the image jpg file
                response_code = response_code.encode("utf-8") + data
                # Sends the 200 response to the connection to display the image jpg file on to the html file
                connection.send(response_code)
            # If the opening of the requested image was unsuccessful, it means that the image was not found and so a 404 response is issued
            # Normally the html page will show a broken image icon which indicates that the image was unsuccessful in loading
            except FileNotFoundError:
                # Runs the send_404_page method to send the appropriate 404 response to the connection
                send_404_page(connection)
    # Closes the connection after successfully getting the requested file or failing to by the 404 response
    connection.close()


####################################
# Input: connection
# Output: None
# Purpose: Creates the appropriate response for the 404 error using a custom 404 page and sends it to the connection
####################################
def send_404_page(connection):
    # Opens the 404_page.html located in the same directory as the source code
    with open('404_page.html', "rb") as file:
        # Reads and stores the contents of the 404_page.html
        data = file.read()
    # Sets the response to 404 status code
    response_code = STATUS_404
    # Adds that the content is a html text file, specially the custom 404 page
    response_code += "Content-Type: text/html\r\n"
    # Adds what the length of the contents of the 404 page will be in bytes
    response_code += "Content-Length: {}\r\n\r\n".format(len(data))
    # Encode the response in standard utf-8 and adds the data of the 404 page
    response_code = response_code.encode("utf-8") + data
    # Sends the 404 to the connection which should display the custom 404 page into the browser
    connection.send(response_code)


####################################
# Input: None
# Output: None
# Purpose: # Starts the server and connection
####################################
def server():
    # Used https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/ as reference
    # for creating the clientSocket, binding, listening, and the while true loop for waiting for a connection

    # Create a TCP/IP socket, AF_INET for IPv4 address protocol, SOCK_STREAM for socket type
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port number
    clientSocket.bind((IP, PORT))
    # Sets the socket to listen for connections
    clientSocket.listen(1)
    # Prints that the server is waiting for a connection
    print("Waiting for a connection...")

    # Loops forever and waits for a connection typically by the browser
    while True:
        # Accepts a connection from the client by the browser
        connection, client_address = clientSocket.accept()
        # Prints that the connection was accepted
        print("Connection Accepted")

        # Used https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python as reference for
        # how to create a thread for the client connections and start them.
        # Creates the thread for the handling of the connection from the client
        clientThread = threading.Thread(target=client_thread, args=(connection,))
        # Starts the client thread which runs the handle_client method to handle the connection and send a response
        clientThread.start()


# Runs the server method to start the client connection
server()
