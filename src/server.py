import time
import socket
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
server_state = Estado()

def handle_client(state, client_socket, client_address):
    send_message(client_socket, 1)
    send_message(client_socket, f'Informe seu nome, por favor.\n')
    nome_jogador = receive_message(client_socket, 1024)
    state.estados_clientes[(client_address[0], client_address[1])] = Estado_Cliente(nome_jogador, client_socket)
    # Lida com as comunicações com um cliente específico
    send_message(client_socket, f'Envie 1 quando estiver pronto, ou qualquer outro valor para desconectar\n')
    data = receive_message(client_socket, 1)
    if data == '1':
        state.estados_clientes[(client_address[0], client_address[1])].pronto = True
    else:
        client_socket.close()
        state.estados_clientes.pop((client_address[0], client_address[1]))

def solicitar_mao(state, client_socket, chave):
    send_message(client_socket, 2)
    send_message(client_socket, 'Informe a quantidade de palitos da mão atual:')
    qntMao = int(receive_message(client_socket, 1))
    while not 0 <= int(qntMao) <= 3:
        resultado = 0
        send_message(client_socket, resultado)
        send_message(client_socket, 'Quantidade inválida. Digite um valor de 0 até 3:')
        qntMao = int(receive_message(client_socket, 1))
    resultado = 1
    send_message(client_socket, resultado)
    state.quantidade_palitos += int(qntMao)
    server_state.estados_clientes[chave].informou_mao = True



def start_server(host, port):
    # Cria um soquete TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Vincula o soquete à interface local e ao número da porta
    server_socket.bind((host, port))
    # Inicia o modo passivo e define o limite de conexões em fila
    server_socket.listen(5)
    print(f'Servidor escutando em {host}:{port}...')

    while server_state.estagio == 1:
        # Aguarda uma nova conexão
        client_socket, client_address = server_socket.accept()
        print(f'Nova conexão de {client_address[0]}:{client_address[1]}')
        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(server_state, client_socket, client_address,))
        client_thread.start()


def pre_jogo():
    if len(server_state.estados_clientes) >= 2 and all(chr.pronto for chr in server_state.estados_clientes.values()):
        server_state.estagio = 2

def mao():
    server_state.quantidade_palitos = 0
    for chave, valor in server_state.estados_clientes.items():
      valor.quantidade_palitos_palpite = -1
      valor.informou_mao = False
      server_state.estados_clientes[chave] = valor
      if not valor.acertou:
        client_thread = threading.Thread(target=solicitar_mao, args=(server_state, server_state.estados_clientes[chave].client_socket, chave, ))
        client_thread.start()
    server_state.estagio = 3

def palpites():
    if all(chr.informou_mao for chr in server_state.estados_clientes.values()):
        for chave, valor in server_state.estados_clientes.items():
            nome_palpitante = valor.nome_jogador
            client_socket = server_state.estados_clientes[chave].client_socket
            send_message(client_socket, 3)
            message = 'Informe seu palpite: '
            send_message(client_socket, message)
            qt_palpite = int(receive_message(client_socket, 1))
            while any(chr.quantidade_palitos_palpite == int(qt_palpite) for chr in server_state.estados_clientes.values()):
                retorno = 0
                send_message(client_socket, retorno)
                send_message(client_socket, 'Palpite já foi dado por outra pessoa. Informe seu palpite:')
                qt_palpite = int(receive_message(client_socket, 1))
            retorno = 1
            send_message(client_socket, retorno)
            valor.quantidade_palitos_palpite = int(qt_palpite)
            server_state.estados_clientes[chave] = valor
            informar_palpite(nome_palpitante, qt_palpite)
            time.sleep(1)
        server_state.estagio = 4

def informar_palpite(nome_jogador, qt_palpite):
    for chave, valor in server_state.estados_clientes.items():
        client_socket = server_state.estados_clientes[chave].client_socket
        send_message(client_socket, 6)
        send_message(client_socket, f'Palpite de {nome_jogador}: {qt_palpite}\n')

def resultado():
    nome_vencedor = ''
    mensagem = ''
    for chave, valor in server_state.estados_clientes.items():
        if server_state.quantidade_palitos == server_state.estados_clientes[chave].quantidade_palitos_palpite:
            nome_vencedor = server_state.estados_clientes[chave].nome_jogador
            server_state.estados_clientes[chave].acertou = True
            break
    if nome_vencedor == '':
        mensagem = f'Não houveram vencedores nesta rodade. Quantidade total: {server_state.quantidade_palitos}'
    else:
        mensagem = f'Vencedor da rodada: {nome_vencedor}. Quantidade total: {server_state.quantidade_palitos}'
    for chave, valor in server_state.estados_clientes.items():
        client_socket = server_state.estados_clientes[chave].client_socket
        send_message(client_socket, 4)
        send_message(client_socket, mensagem)
    sobrou = {chave: valor for chave, valor in server_state.estados_clientes.items() if not valor.acertou }
    if len(sobrou) <= 1:
        nome_pato = ''
        for chave, valor in server_state.estados_clientes.items():
            if not valor.acertou:
                nome_pato = valor.nome_jogador
        for chave, valor in server_state.estados_clientes.items():
            client_socket = server_state.estados_clientes[chave].client_socket
            send_message(client_socket, 5)
            send_message(client_socket, f'Pato: {nome_pato}')
        server_state.estagio = 5
    else:
        server_state.estagio = 2
        
def watch_state():
    while not server_state.estagio == 5:
        if server_state.estagio == 1:
            pre_jogo()
        if server_state.estagio == 2:
            mao()
        if server_state.estagio == 3:
            palpites()
        if server_state.estagio == 4:
            resultado()




# Configurações do servidor
HOST = socket.gethostbyname(socket.gethostname())  # Endereço IP do servidor
PORT = 12345  # Porta do servidor


client_thread = threading.Thread(target=start_server, args=(HOST, PORT))
client_thread.start()

watch_state()


