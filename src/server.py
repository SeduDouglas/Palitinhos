import socket
import threading
from objects.classes.estado import Estado
from objects.classes.estado_cliente import Estado_Cliente
from objects.enums.estagio import Estagio
from objects.enums.solicitacao_comunicacao import Solicitacao_Comunicacao

server_state = Estado()

def handle_client(state, client_socket, client_address):
    client_socket.send(Solicitacao_Comunicacao.CONEXAO.encode('utf-8'))
    conect_response = f'Informe seu nome, por favor.'
    client_socket.send(conect_response.encode('utf-8'))
    nome_jogador = client_socket.recv(1024).decode('utf-8')
    state.estados_clientes[(client_address[0], client_address[1])] = Estado_Cliente(nome_jogador, client_socket)
    # Lida com as comunicações com um cliente específico
    response = f'Envie 1 quando estiver pronto, ou qualquer outro valor para desconectar'
    client_socket.send(response.encode('utf-8'))
    # Aguarda a mensagem do cliente
    data = client_socket.recv(1024).decode('utf-8')
    if data == '1':
        state.estados_clientes[(client_address[0], client_address[1])].pronto = True
    else:
        client_socket.close()
        state.estados_clientes.pop((client_address[0], client_address[1]))

def solicitar_mao(state, client_socket, chave):
    client_socket.send(Solicitacao_Comunicacao.MAO.encode('utf-8'))
    message = 'Informe a quantidade de palitos da mão atual:'
    client_socket.send(message.encode('utf-8'))
    qntMao = client_socket.recv(1024).decode('utf-8')
    while not 0 <= qntMao <= 3:
        resultado = 0
        client_socket.send(resultado.encode('utf-8'))
        message = 'Quantidade inválida. Digite um valor de 0 até 3:'
        client_socket.send(message.encode('utf-8'))
        qntMao = client_socket.recv(1024).decode('utf-8')
    resultado = 1
    client_socket.send(resultado.encode('utf-8'))
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

    while server_state.estagio.PRE_JOGO:
        # Aguarda uma nova conexão
        client_socket, client_address = server_socket.accept()
        print(f'Nova conexão de {client_address[0]}:{client_address[1]}')
        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(server_state, client_socket, client_address,))
        client_thread.start()


def pre_jogo():
    if len(server_state.estados_clientes) >= 2 and all(chr.pronto for chr in server_state.estados_clientes.values()):
        server_state.estagio = Estagio.MAO

def mao():
    server_state.quantidade_palitos = 0
    for chave, valor in server_state.estados_clientes.items():
      valor.quantidade_palitos_palpite = -1
      valor.informou_mao = False
      server_state.estados_clientes[chave] = valor
      if not valor.acertou:
        client_thread = threading.Thread(target=solicitar_mao, args=(server_state, server_state.estados_clientes[chave].client_socket, chave, ))
        client_thread.start()
    server_state.estagio = Estagio.PALPITES

def palpites():
    if all(chr.informou_mao for chr in server_state.estados_clientes.values()):
        for chave, valor in server_state.estados_clientes.items():
            nome_palpitante = valor.nome_jogador
            server_state.estados_clientes[chave].client_socket.send(Solicitacao_Comunicacao.PALPITES.encode('utf-8'))
            message = 'Informe seu palpite:'
            server_state.estados_clientes[chave].client_socket.send(message.encode('utf-8'))
            qt_palpite = server_state.estados_clientes[chave].client_socket.recv(1024).decode('utf-8')
            while any(chr.quantidade_palitos_palpite == int(qt_palpite) for chr in server_state.estados_clientes.values()):
                retorno = 0
                server_state.estados_clientes[chave].client_socket.send(retorno.encode('utf-8'))
                message = 'Palpite já foi dado por outra pessoa. Informe seu palpite:'
                server_state.estados_clientes[chave].client_socket.send(message.encode('utf-8'))
                qt_palpite = server_state.estados_clientes[chave].client_socket.recv(1024).decode('utf-8')
            retorno = 0
            server_state.estados_clientes[chave].client_socket.send(retorno.encode('utf-8'))
            valor.quantidade_palitos_palpite = int(qt_palpite)
            server_state.estados_clientes[chave] = valor
            informar_palpite(nome_palpitante, qt_palpite)
        server_state.estagio = Estagio.RESULTADO

def informar_palpite(nome_jogador, qt_palpite):
    for chave, valor in server_state.estados_clientes.items():
        server_state.estados_clientes[chave].client_socket.send(Solicitacao_Comunicacao.INFORMAR_PALPITE.encode('utf-8'))
        message = f'Palpite de {nome_jogador}: {qt_palpite}'
        server_state.estados_clientes[chave].client_socket.send(message.encode('utf-8'))

def resultado():
    nome_vencedor = ''
    for chave, valor in server_state.estados_clientes.items():
        if server_state.quantidade_palitos == server_state.estados_clientes[chave].quantidade_palitos_palpite:
            nome_vencedor = server_state.estados_clientes[chave].nome_jogador
            server_state.estados_clientes[chave].acertou = True
            break
    for chave, valor in server_state.estados_clientes.items():
        server_state.estados_clientes[chave].client_socket.send(Solicitacao_Comunicacao.RESULTADO.encode('utf-8'))
        mensagem = f'Vencedor da rodada: {nome_vencedor}'
        server_state.estados_clientes[chave].client_socket.send(mensagem.encode('utf-8'))
    sobrou = {chave: valor for chave, valor in server_state.estados_clientes.items() if valor.acertou }
    if len(sobrou) <= 1:
        for chave, valor in server_state.estados_clientes.items():
          server_state.estados_clientes[chave].client_socket.send(Solicitacao_Comunicacao.FIM.encode('utf-8'))
          mensagem = f'Pato: {valor.nome_jogador}'
          server_state.estados_clientes[chave].client_socket.send(mensagem.encode('utf-8'))
        server_state.estagio = Estagio.FIM
    else:
        server_state.estagio = Estagio.MAO
        
def watch_state():
    while not server_state.estagio.FIM:
        if server_state.estagio == Estagio.PRE_JOGO:
            pre_jogo()
        if server_state.estagio == Estagio.MAO:
            mao()
        if server_state.estagio == Estagio.PALPITES:
            palpites()
        if server_state.estagio == Estagio.RESULTADO:
            resultado()




# Configurações do servidor
HOST = socket.gethostbyname(socket.gethostname())  # Endereço IP do servidor
PORT = 12345  # Porta do servidor


client_thread = threading.Thread(target=start_server, args=(HOST, PORT))
client_thread.start()

watch_state()


