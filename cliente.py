import socket
from time import sleep

host = '10.1.24.153'  
port = 12345 


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client_socket.connect((host, port))
print(f"Conectado ao servidor {host}:{port}")

try:

    while True:
        message = "Olá, servidor!"
        client_socket.send(message.encode())


        data = client_socket.recv(1024)
        print(f"Resposta do servidor: {data.decode()}")

        sleep(1)

except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:

    client_socket.close()
