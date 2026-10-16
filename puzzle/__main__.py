import pygame
import os

from puzzle.settings import COR_DESTAQUE, TAMANHO
from . import settings as cfg
from .niveis import carrega_nivel

def desenha_casa(tela, col, linha, cor):
    """ Converte (coluna, linha) em pixels e desenha um quadrado. """
    retangulo = pygame.Rect(
        col * cfg.TAMANHO,
        linha * cfg.TAMANHO,
        cfg.TAMANHO - 2, #o valor -2 deixa um espaço entre casas
        cfg.TAMANHO - 2
    )
    pygame.draw.rect(tela, cor, retangulo)
    
def dentro_da_grade(pos):
    """ Fala se uma possição (coluna, linha) está dentro do tabuleiro. """
    col, linha = pos
    return 0 <= col < cfg.COLUNAS and 0 <= linha < cfg.LINHAS

def tenta_andar(jogador, dc, dl, paredes, caixas):
    """ Tenta mover o jogador, empurando caixas se necessário. Retorna True se o jogador se moveu."""
    destino = (jogador[0] + dc, jogador[1] + dl)
    
    
    # 1) junta as caixas a frente do jogador, se houverem
    fila = []
    atual = destino
    while atual in caixas:
        fila.append(atual)
        atual = (atual[0] + dc, atual[1] + dl)
        
    # 2) "atual" agora é a primeira casa DEPOIS da fila
    #    (ou o próprio destino, se não havia nenhuma caixa).
    #    Ela precisa estar dentro da grade e não ser parede.    
    if not dentro_da_grade(atual) or atual in paredes:
        return False

    # 3) move as caixas da ultima para a primeira 
    for caixa in reversed(fila):
        caixas.remove(caixa)
        caixas.add((caixa[0] + dc, caixa[1] + dl))
        
    # 4) move o jogador
    jogador[0], jogador[1] = destino
    return True

def cria_camada_grade():
    """ Monta uma vez uma imagem transparente com a grade e as coordenadas. 
    
    Oque não muda a cada frame, desenhamos uma vez só e reaproveitamos.
    """
    
    largura = cfg.COLUNAS * cfg.TAMANHO
    altura = cfg.LINHAS * cfg.TAMANHO
    #SCRALPHA = supreficie com transparencia: so o que desenha aparece
    camada = pygame.Surface((largura, altura), pygame.SRCALPHA)
    fonte_pequena = pygame.font.Font(None, 20)
    
    for col in range(cfg.COLUNAS):
        for linha in range(cfg.LINHAS):
            retangulo = pygame.Rect(
                col * cfg.TAMANHO, linha * cfg.TAMANHO, cfg.TAMANHO, cfg.TAMANHO
            )
            pygame.draw.rect(camada, cfg.COR_GRADE, retangulo, 1) # 1 é so o contorno
            texto = fonte_pequena.render(f"{col},{linha}", True, cfg.COR_COORDENADAS)
            camada.blit(texto, (retangulo.x + 3, retangulo.y + 3))
        return camada

def main():
    pygame.init()
    tela = pygame.display.set_mode((cfg.COLUNAS * cfg.TAMANHO, cfg.LINHAS * cfg.TAMANHO))
    pygame.display.set_caption(cfg.TITULO)
    relogio = pygame.time.Clock()
    
    # Estado do game
    caminho_nivel = cfg.PASTA_NIVEIS / "nivel_02.txt"
    jogador, paredes, caixas, bandeira = carrega_nivel(caminho_nivel)
    venceu = False
    mostrar_grade = False
    camada_grade = cria_camada_grade()
    
    
    try:
        font = pygame.font.Font(cfg.PASTA_FONTE / "PixelifySans-Medium.ttf", 25)
    except FileNotFoundError:
        print(f"Fonte não encontrada em {cfg.PASTA_FONTE / 'PixelifySans-Medium.ttf'}. Usando a fonte padrão.")
        font = pygame.font.Font(None, 25)
    
    rodando = True
    while rodando:
        
        #Fase 1 + 2 Eventos e logica
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_g:
                mostrar_grade = not mostrar_grade  #liga/desliga a grade
            
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                try:
                    # essa atribuição so acontece quando carrega_nivel não der erro 
                    # se der o nivel atual continua valendo.
                    jogador, paredes, caixas, bandeira = carrega_nivel(caminho_nivel)
                    venceu = False
                except ValueError as error:
                    print(f"Erro no nivel: {error}")
            
            if evento.type == pygame.KEYDOWN and not venceu:
                dc, dl = 0, 0
                if evento.key == pygame.K_LEFT:
                    dc = -1
                elif evento.key == pygame.K_RIGHT:
                    dc = 1
                elif evento.key == pygame.K_UP:
                    dl = -1
                elif evento.key == pygame.K_DOWN:
                    dl = 1
                
                if (dc, dl) != (0, 0):
                    tenta_andar(jogador, dc, dl, paredes, caixas)
                
                
                if(tuple(jogador) == bandeira):
                    venceu = True
                
                                     
        #Fase 3 DESENHAR
        tela.fill(cfg.COR_FUNDO)
        
        for col, linha in paredes:
            desenha_casa(tela, col, linha, cfg.COR_PAREDE)
            
        desenha_casa(tela, bandeira[0], bandeira[1], cfg.COR_BANDEIRA)
        
        for col, linha in caixas:
            desenha_casa(tela, col, linha, cfg.COR_CAIXA)
        
        desenha_casa(tela, jogador[0], jogador[1], cfg.COR_JOGADOR)
        
        if mostrar_grade:
            tela.blit(camada_grade, (0, 0))
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col_mouse = mouse_x // cfg.TAMANHO
            linha_mouse = mouse_y // cfg.TAMANHO
            destaque = pygame.Rect(
                col_mouse * cfg.TAMANHO, linha_mouse * cfg.TAMANHO,
                cfg.TAMANHO, cfg.TAMANHO
            )
            pygame.draw.rect(tela, cfg.COR_DESTAQUE, destaque, 2) # 2 é a largura do contorno
        
        if venceu:
            texto = font.render("Você pegou a bandeira!", True, (255, 255, 255))
            tela.blit(texto, (100, 100))
        
        pygame.display.flip()
        relogio.tick(cfg.FPS)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()