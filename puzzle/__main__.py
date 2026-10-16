import pygame
import os

from . import settings as cfg

def desenha_casa(tela, col, linha, cor):
    """ Converte (coluna, linha) em pixels e desenha um quadrado. """
    retangulo = pygame.Rect(
        col * cfg.TAMANHO,
        linha * cfg.TAMANHO,
        cfg.TAMANHO - 2, #o valor -2 deixa um espaço entre casas
        cfg.TAMANHO - 2
    )
    pygame.draw.rect(tela, cor, retangulo)
    
def main():
    pygame.init()
    tela = pygame.display.set_mode((cfg.COLUNAS * cfg.TAMANHO, cfg.LINHAS * cfg.TAMANHO))
    pygame.display.set_caption(cfg.TITULO)
    relogio = pygame.time.Clock()
    
    # Estado do game
    
    jogador = [2, 5] # coluna e linha
    paredes = {(5, 3), (5, 4), (5, 5), (5, 6), (8, 8), (9, 8)}
    bandeira = (12, 10)
    venceu = False
    
    caminho_fonte = os.path.join("assets", "fonts", "PixelifySans-Medium.ttf")
    
    try:
        font = pygame.font.Font(caminho_fonte, 25)
    except FileNotFoundError:
        print(f"Fonte não encontrada em {caminho_fonte}. Usando a fonte padrão.")
        font = pygame.font.Font("None", 25)
    
    rodando = True
    while rodando:
        
        #Fase 1 + 2 Eventos e logica
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
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
                
                nova_col = jogador[0] + dc
                nova_linha = jogador[1] + dl
                
                dentro  = 0 <= nova_col < cfg.COLUNAS and 0 <= nova_linha <  cfg.LINHAS
                if dentro and (nova_col, nova_linha) not in paredes:
                    jogador[0] = nova_col
                    jogador[1] = nova_linha
                
                if(tuple(jogador) == bandeira):
                    venceu = True
                
            
                
                
        #Fase 3 DESENHAR
        tela.fill(cfg.COR_FUNDO)
        
        for col, linha in paredes:
            desenha_casa(tela, col, linha, cfg.COR_PAREDE)
            
        desenha_casa(tela, bandeira[0], bandeira[1], cfg.COR_BANDEIRA)
        desenha_casa(tela, jogador[0], jogador[1], cfg.COR_JOGADOR)
        
        if venceu:
            texto = font.render("Você pegou a bandeira!", True, (255, 255, 255))
            tela.blit(texto, (100, 100))
        
        pygame.display.flip()
        relogio.tick(cfg.FPS)
    
    pygame.quit()
    
if __name__ == "__main__":
    main()