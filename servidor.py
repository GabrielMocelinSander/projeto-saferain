import socket
import requests

host = '0.0.0.0' 
port = 12345 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))

server_socket.listen(1)
print(f"Aguardando conexao na porta {port}...")

client_socket, client_address = server_socket.accept()
print(f"Conexao estabelecida com {client_address}")

try:
 
    while True:
        
        API_KEY="e331ab67a05b53fa1918ac0d9fcbcf24"
        cidade = "passo fundo"
        link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"
        
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        
        print(requisicao_dic)
        
        descricao = requisicao_dic['weather'][0]['description']
        temperatura = requisicao_dic['main']['temp'] - 273.15
        formatted_number = "{:.2f}".format(temperatura)
        data = client_socket.recv(1024)  
        if not data:
            break
        print(f"Mensagem recebida: {data.decode()}")
        

        response = f"{descricao} | { formatted_number} Graus"        
        client_socket.send(response.encode())

except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    client_socket.close()
    server_socket.close()
