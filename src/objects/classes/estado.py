
from objects.enums.estagio import Estagio

class Estado:
    def __init__(self):
        self.estagio = 1
        self.quantidade_palitos = 0
        self.estados_clientes = {}
        self.vencedor_rodada = ''