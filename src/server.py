import socket
import threading

def handle_client(state, client_socket):
    # Lida com as comunicações com um cliente específico
    while True:
        # Aguarda a mensagem do cliente
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            # Se nenhum dado for recebido, a conexão foi encerrada
            break
        print(f'Mensagem recebida do cliente: {data}')
        # Envie uma resposta de volta para o cliente
        response = f'Recebido: {data}'
        client_socket.send(response.encode('utf-8'))
    # Fecha o soquete do cliente após a comunicação
    client_socket.close()

def start_server(host, port):
    # Cria um soquete TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Vincula o soquete à interface local e ao número da porta
    server_socket.bind((host, port))
    # Inicia o modo passivo e define o limite de conexões em fila
    server_socket.listen(5)
    print(f'Servidor escutando em {host}:{port}...')

    while True:
        # Aguarda uma nova conexão
        client_socket, client_address = server_socket.accept()
        print(f'Nova conexão de {client_address[0]}:{client_address[1]}')
        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Configurações do servidor
HOST = socket.gethostbyname(socket.gethostname())  # Endereço IP do servidor
PORT = 12345  # Porta do servidor

# Inicia o servidor
start_server(HOST, PORT)