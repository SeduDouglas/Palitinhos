import socket
import threading
from objects.classes.estado import Estado
from objects.classes.estado_cliente import Estado_Cliente
from objects.enums.estagio import Estagio
from objects.enums.solicitacao_comunicacao import Solicitacao_Comunicacao


fim = False
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

def palpites():
    retorno = 0
    while resultado == 0:
      mensagem = client_socket.recv(1024).decode('utf-8')
      nome = input(mensagem)
      client_socket.send(nome.encode('utf-8'))
      resultado = int(client_socket.recv(1024).decode('utf-8'))

def informar_palpite():
  mensagem = client_socket.recv(1024).decode('utf-8')
  print(f'{mensagem}')

def resultado():
      mensagem = client_socket.recv(1024).decode('utf-8')
      print(f'{mensagem}')

def fim():
      mensagem = client_socket.recv(1024).decode('utf-8')
      print(f'{mensagem}')
      fim = True


# Configurações do cliente
HOST = '192.168.137.1'  # Endereço IP do servidor
PORT = 12345  # Porta do servidor

# Cria um soquete TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print(f'Conectado ao servidor {HOST}:{PORT}')

while not fim:
    # Aguarda a resposta do servidor
    command = int(client_socket.recv(1024).decode('utf-8'))
    if Solicitacao_Comunicacao.CONEXAO == command:
      conexao()
    if Solicitacao_Comunicacao.MAO == command:
        mao()
    if Solicitacao_Comunicacao.PALPITES == command:
        palpites()
    if Solicitacao_Comunicacao.RESULTADO == command:
        resultado()
    if Solicitacao_Comunicacao.FIM == command:
        fim()
    if Solicitacao_Comunicacao.INFORMAR_PALPITE == command:
        informar_palpite()

# Fecha o soquete do cliente
client_socket.close()