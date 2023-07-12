
class Estado_Cliente:
    def __init__(self, nome_jogador, client_socket):
        self.quantidade_palitos_palpite = -1
        self.nome_jogador = nome_jogador
        self.acertou = False
        self.pronto = False
        self.client_socket = client_socket
        self.informou_mao = False