from socket import *
import threading
import random
import json

def handleClient(connectionSocket, address):
    print(address)
    while True:
        # Receive JSON request from client
        json_data = connectionSocket.recv(1024).decode()
        request = json.loads(json_data)

        method = request.get("method", "").strip().lower()

        if method == 'random':
            num1 = request.get("Tal1", 1)
            num2 = request.get("Tal2", 10)
            print(f"Received numbers: {num1}, {num2}")
            random_number = random.randint(num1, num2)
            response = {"result": random_number}

        elif method == 'add':
            num1 = request.get("Tal1", 0)
            num2 = request.get("Tal2", 0)
            print(f"Received numbers: {num1}, {num2}")
            result = num1 + num2
            response = {"result": result}

        elif method == 'subtract':
            num1 = request.get("Tal1", 0)
            num2 = request.get("Tal2", 0)
            print(f"Received numbers: {num1}, {num2}")
            result = num1 - num2
            response = {"result": result}

        else:
            response = {"error": "Invalid method"}

        # Encode response as JSON and send to client
        connectionSocket.send(json.dumps(response).encode())
    
    connectionSocket.close()

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket, addr)).start()