from enum import Enum

class Solicitacao_Comunicacao(Enum):
    CONEXAO = 1
    MAO = 2
    PALPITES = 3
    RESULTADO = 4
    FIM = 5
    INFORMAR_PALPITE = 6