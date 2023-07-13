import socket
import time
import threading
from objects.classes.estado import Estado
from objects.classes.estado_cliente import Estado_Cliente
from objects.enums.estagio import Estagio
from objects.enums.solicitacao_comunicacao import Solicitacao_Comunicacao

def send_message(client_socket, message):
    client_socket.send(str(message).encode('utf-8'))
    time.sleep(1)

def receive_message(client_socket, size):
    message = client_socket.recv(size).decode('utf-8')
    time.sleep(1)
    return message
naoFim = True
def conexao(client_socket):
    mensagem = receive_message(client_socket, 1024)
    nome = input(mensagem)
    client_socket.send(nome.encode('utf-8'))
    mensagem = receive_message(client_socket, 1024)
    pronto = input(mensagem)
    send_message(client_socket, pronto)

def mao(client_socket):
    resultado = 0
    while resultado == 0:
      mensagem = receive_message(client_socket, 1024)
      mao = input(mensagem)
      send_message(client_socket, mao)
      resultado = int(receive_message(client_socket, 1))

def palpites(client_socket):
    resultado = 0
    while resultado == 0:
      mensagem = receive_message(client_socket, 1024)
      palpite = input(mensagem)
      send_message(client_socket, palpite)
      resultado = int(receive_message(client_socket, 1))

def informar_palpite(client_socket):
  mensagem = receive_message(client_socket, 1024)
  print(f'{mensagem}')

def resultado(client_socket):
      mensagem = receive_message(client_socket, 1024)
      print(f'{mensagem}')

def fim(client_socket):
      mensagem = receive_message(client_socket, 1024)
      print(f'{mensagem}')
      naoFim = False


# Configurações do cliente
HOST = '192.168.137.1'  # Endereço IP do servidor
PORT = 12345  # Porta do servidor

# Cria um soquete TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print(f'Conectado ao servidor {HOST}:{PORT}')

while naoFim:
    # Aguarda a resposta do servidor
    command = client_socket.recv(1).decode('utf-8')
    if 1 == int(command):
        conexao(client_socket)
    if 2 == int(command):
        mao(client_socket)
    if 3 == int(command):
        palpites(client_socket)
    if 4 == int(command):
        resultado(client_socket)
    if 5 == int(command):
        fim(client_socket)
    if 6 == int(command):
        informar_palpite(client_socket)

# Fecha o soquete do cliente
client_socket.close()