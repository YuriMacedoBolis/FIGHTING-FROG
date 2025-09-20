import pygame
from config import *


def carregar_imagem(caminho, largura, altura):
    imagem = pygame.image.load(caminho).convert_alpha()
    imagem = pygame.transform.scale(imagem, (largura, altura))
    return imagem

def virar_imagem(caminho, largura, altura):
    imagem = carregar_imagem(caminho, largura, altura)
    return pygame.transform.flip(imagem, True, False)

def tela_inicio(janela):
    capa = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Fundo\\Capa.png",676,455)
    capa_rect = capa.get_rect(center=(LARGURA/2 , ALTURA/2 - 100))
    fundo_inicio = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Fundo\\Cenario_beco_borrado.png" , LARGURA , ALTURA)
    fonte = pygame.font.SysFont("Arial" , 25 , bold=True)
    texto = fonte.render("Por Yuri Macedo Bolis" ,True , BRANCO)
    texto_rect = texto.get_rect(center=(150 , 680))
    botao_img = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Botões\\Botao_Jogar.png" , 345 , 345)
    botao_hover = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Botões\\Botao_Jogar_hover.png" , 345 , 345)
    imagem_atual = botao_img

    botao_rect = botao_img.get_rect(center=(LARGURA/2 , ALTURA/2 + 170))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(mouse_pos):
                    return True

        if botao_rect.collidepoint(mouse_pos):
            imagem_atual = botao_hover
        else:
            imagem_atual = botao_img

        janela.blit(fundo_inicio , (0,0))
        janela.blit(capa , capa_rect)
        janela.blit(imagem_atual , botao_rect)
        janela.blit(texto , texto_rect)
        pygame.display.flip()

def tela_game_over(janela , pontuacao , rodada):
    #FUNDO
    fundo_game_over = carregar_imagem('PROJETO_JOGO\\IMAGENS PISKEL\\Fundo\\Cenario_beco_borrado.png',LARGURA , ALTURA)

    #BOTÕES
    botao_jogar_novamente = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Botões\\Botao_game_over.png" , 288,288)
    botao_jogar_novamente_hover = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Botões\\Botao_game_over_hover.png" , 288 , 288)
    img_atual = botao_jogar_novamente

    fonte_titulo = pygame.font.SysFont("Arial" , 100 , bold=True)
    fonte_corpo = pygame.font.SysFont("Arial" , 50 , bold=True)
    texto_game_over = fonte_titulo.render("FIM DE JOGO" , True , BRANCO)
    texto_pontuacao = fonte_corpo.render(f"PONTUAÇÃO: {pontuacao}" , True , BRANCO)
    texto_rodada = fonte_corpo.render(f"RODADAS: {rodada}" ,True , BRANCO)
    
    rect_pontuacao = texto_pontuacao.get_rect(center=(LARGURA/2 , ALTURA/2 -50))
    texto_rect = texto_game_over.get_rect(center=(LARGURA/2 , ALTURA/2 -200))
    texto_rodada_rect = texto_rodada.get_rect(center=(LARGURA/2 , ALTURA/2 +50))
    botao_rect = img_atual.get_rect(center=(LARGURA/2 , ALTURA/2 +150))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(mouse_pos):
                    return True

        if botao_rect.collidepoint(mouse_pos):
            img_atual = botao_jogar_novamente_hover

        else:
            img_atual = botao_jogar_novamente

        janela.blit(fundo_game_over , (0,0))
        janela.blit(texto_pontuacao , rect_pontuacao)
        janela.blit(texto_game_over , texto_rect)
        janela.blit(texto_rodada , texto_rodada_rect)
        janela.blit(img_atual , botao_rect)
        pygame.display.flip() 