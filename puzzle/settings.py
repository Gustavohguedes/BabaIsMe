# puzzle todas as constantes do jogo ficam aqui 
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TITULO = "Meu puzzle"
FPS = 60
PASTA_NIVEIS = RAIZ / "levels"
PASTA_FONTE = RAIZ / "assets" / "fonts"

#Grade
TAMANHO = 48
COLUNAS = 16
LINHAS = 12

# cores

COR_FUNDO = (20, 20, 30)
COR_PAREDE = (110, 110, 130)
COR_JOGADOR = (0, 200, 120)
COR_BANDEIRA = (255, 215, 0)
COR_CAIXA = (170, 110, 60)


# Modo de grade
COR_GRADE = (60, 60, 80)
COR_COORDENADAS = (140, 140, 170)
COR_DESTAQUE = (255, 255, 255)