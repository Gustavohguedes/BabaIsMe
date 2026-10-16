# puzzle/niveis.py
from . import settings as cfg



def carrega_nivel(caminho):
    """Lê um nível desenhado em texto e devolve (jogador, paredes, caixas, bandeira).

    Legenda:  .  vazio   #  parede   C  caixa   P  jogador   F  bandeira
    """
    # "with" abre o arquivo e GARANTE que ele será fechado no final,
    # mesmo se der erro no meio (parecido com try/finally).
    with open(caminho, encoding="utf-8") as arquivo:
        linhas = arquivo.read().splitlines()   # lista com uma string por linha

    # Validação: um nível torto (linha com caractere a mais ou a menos)
    # desalinharia tudo. Melhor avisar do que desenhar errado em silêncio.
    if len(linhas) != cfg.LINHAS:
        raise ValueError(f"{caminho.name}: esperava {cfg.LINHAS} linhas, achei {len(linhas)}")
    for numero, texto in enumerate(linhas):
        if len(texto) != cfg.COLUNAS:
            raise ValueError(
                f"{caminho.name}, linha {numero}: "
                f"esperava {cfg.COLUNAS} colunas, achei {len(texto)}"
            )

    paredes = set()
    caixas = set()
    jogador = None
    bandeira = None

    # enumerate() entrega (posição, conteúdo) de cada item de uma lista.
    # Loop de fora: cada linha do desenho. Loop de dentro: cada caractere.
    for linha, texto in enumerate(linhas):
        for col, simbolo in enumerate(texto):
            if simbolo == "#":
                paredes.add((col, linha))
            elif simbolo == "C":
                caixas.add((col, linha))
            elif simbolo == "P":
                jogador = [col, linha]     # lista: o jogador se move
            elif simbolo == "F":
                bandeira = (col, linha)    # tupla: a bandeira é fixa

    if jogador is None or bandeira is None:
        raise ValueError(f"{caminho.name}: o nível precisa de um P (jogador) e um F (bandeira)")

    return jogador, paredes, caixas, bandeira