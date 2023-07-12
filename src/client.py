import socket
import threading
from objects.classes.estado import Estado
from objects.classes.estado_cliente import Estado_Cliente
from objects.enums.estagio import Estagio
from objects.enums.solicitacao_comunicacao import Solicitacao_Comunicacao


naoFim = True
def conexao(client_socket):
    mensagem = client_socket.recv(1024).decode('utf-8')
    nome = input(mensagem)
    client_socket.send(nome.encode('utf-8'))
    mensagem = client_socket.recv(1024).decode('utf-8')
    pronto = input(mensagem)
    client_socket.send(pronto.encode('utf-8'))

def mao(client_socket):
    resultado = 0
    while resultado == 0:
      mensagem = client_socket.recv(1024).decode('utf-8')
      nome = input(mensagem)
      client_socket.send(nome.encode('utf-8'))
      resultado = int(client_socket.recv(1024).decode('utf-8'))

def palpites(client_socket):
    retorno = 0
    while resultado == 0:
      mensagem = client_socket.recv(1024).decode('utf-8')
      nome = input(mensagem)
      client_socket.send(nome.encode('utf-8'))
      resultado = int(client_socket.recv(1024).decode('utf-8'))

def informar_palpite(client_socket):
  mensagem = client_socket.recv(1024).decode('utf-8')
  print(f'{mensagem}')

def resultado(client_socket):
      mensagem = client_socket.recv(1024).decode('utf-8')
      print(f'{mensagem}')

def fim(client_socket):
      mensagem = client_socket.recv(1024).decode('utf-8')
      print(f'{mensagem}')
      naoFim = False


# Configurações do cliente
HOST = '192.168.101.236'  # Endereço IP do servidor
PORT = 12345  # Porta do servidor

# Cria um soquete TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print(f'Conectado ao servidor {HOST}:{PORT}')

while naoFim:
    # Aguarda a resposta do servidor
    command = client_socket.recv(32).decode('utf-8')
    print(command)
    if 1 == int(command):
        conexao(client_socket)
    if Solicitacao_Comunicacao.MAO == command:
        mao(client_socket)
    if Solicitacao_Comunicacao.PALPITES == command:
        palpites(client_socket)
    if Solicitacao_Comunicacao.RESULTADO == command:
        resultado(client_socket)
    if Solicitacao_Comunicacao.FIM == command:
        fim(client_socket)
    if Solicitacao_Comunicacao.INFORMAR_PALPITE == command:
        informar_palpite(client_socket)

# Fecha o soquete do cliente
client_socket.close()