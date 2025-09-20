import pygame
from jogo import Jogo
from config import LARGURA, ALTURA 
from funcoes import *
import asyncio


    
if __name__ == "__main__":
    pygame.init()
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("FIGHTING FROG")
    pygame.display.set_icon(carregar_imagem("PROJETO_JOGO/IMAGENS PISKEL/Sapo/Sapo_hud_5.png",30,30))
    iniciar_jogo = tela_inicio(janela)

    while iniciar_jogo:
        jogo = Jogo(janela)
        jogo.rodar()
        if jogo.jogador.vida <=0:
            iniciar_jogo = tela_game_over(janela , jogo.pontuacao , jogo.rodada_atual)
        else:
            iniciar_jogo = False

    pygame.quit()

