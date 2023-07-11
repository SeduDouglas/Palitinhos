import socket

# Configurações do cliente
HOST = '192.168.137.1'  # Endereço IP do servidor
PORT = 12345  # Porta do servidor

# Cria um soquete TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print(f'Conectado ao servidor {HOST}:{PORT}')

while True:
    # Aguarda a entrada do usuário
    message = input('Digite uma mensagem (ou "sair" para encerrar): ')

    # Envia a mensagem para o servidor
    client_socket.send(message.encode('utf-8'))

    if message.lower() == 'sair':
        # Se o usuário digitar "sair", encerra o cliente
        break

    # Aguarda a resposta do servidor
    response = client_socket.recv(1024).decode('utf-8')
    print(f'Resposta do servidor: {response}')

# Fecha o soquete do cliente
client_socket.close()