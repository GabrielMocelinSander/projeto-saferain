import socket
import requests
import serial
import time
from time import sleep


host = '0.0.0.0'
port = 12345


arduino = serial.Serial('/dev/ttyACM0', 9600)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Aguardando conexao na porta {port}...")

client_socket, client_address = server_socket.accept()
print(f"Conexao estabelecida com {client_address}")

try:
    while True:
       
        API_KEY = "e331ab67a05b53fa1918ac0d9fcbcf24"
        cidade = "Passo Fundo"
        
     
        link = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric"
        
       
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

     
        if requisicao.status_code == 200:
      
            previsao = requisicao_dic['list'][0] 

            descricao = previsao['weather'][0]['description']
            
   
            temperatura = previsao['main']['temp']
            formatted_number = "{:.2f}".format(temperatura)
          
            precip = previsao.get('rain', {}).get('3h', 0)
      
            if precip > 0:
                precip_response = f"Precipitacao: {precip} mm nas ultimas 3 horas"
            else:
                precip_response = "Sem precipitacao nas ultimas 3 horas."
            
            response = f"{descricao} | {formatted_number}graus | {precip_response}"
            client_socket.send(response.encode())
            print(f"Enviado para o cliente: {response}")
  
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip() 
            print(f"Recebido do Arduino: {data}")
  
        sleep(1)

except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    client_socket.close()
    server_socket.close()
