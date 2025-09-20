import pygame
from player import Jogador
from inimigos import Inimigo
from random import randint , choice
from config import *
from funcoes import *

class Jogo():
    def __init__(self, janela):
        self.janela = janela
        self.rodando = True
        self.fundo = pygame.image.load("PROJETO_JOGO\\IMAGENS PISKEL\\Fundo\\Cenario_beco.png")
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))

        self.hud_jogador = carregar_imagem('PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\Sapo_hud_10.png' , 150,150)
        self.hud_rect = self.hud_jogador.get_rect()

        self.todas_sprites = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()

        self.jogador = Jogador(640, 360, self)
        self.todas_sprites.add(self.jogador)

        self.pontuacao = 0
        pygame.font.init()
        self.fonte = pygame.font.SysFont("Arial", 32 , bold=True)
        
        self.ultimo_spawn_time = pygame.time.get_ticks()
        self.intervalo_spawn = 900

        self.rodada_atual = 1
        self.pontuacao_proxima_rodada = 10
        self.velocidade_inimigo = 12

    def spawn_inimigo(self):
        spawn_pontos = {
            "direita": {"x_range": (LARGURA + 50, LARGURA + 100), "y_range": (350, 500), "direcao": "esquerda"},
            "esquerda": {"x_range": (-100, -50), "y_range": (350, 500), "direcao": "direita"},
            "cima": {"x_range": (100, LARGURA - 100), "y_range": (-100, -50), "direcao": "baixo"}
        }

        lado_spawn = choice(list(spawn_pontos.keys()))
        config_spawn = spawn_pontos[lado_spawn]

        x_pos = randint(config_spawn["x_range"][0], config_spawn["x_range"][1])
        y_pos = randint(config_spawn["y_range"][0], config_spawn["y_range"][1])

        velocidade = self.velocidade_inimigo
        vida = 50
        
        if lado_spawn == "cima":
            velocidade += 1
            vida = 25
        
        inimigo = Inimigo(x_pos, y_pos, velocidade, vida, config_spawn["direcao"])
        self.inimigos.add(inimigo)
        self.todas_sprites.add(inimigo)

    def avancar_rodada(self):
        self.rodada_atual += 1
        self.pontuacao_proxima_rodada += 10
        if self.intervalo_spawn >=300:
            self.intervalo_spawn -= 100
        self.velocidade_inimigo += 1

    def desenhar_hud(self):
        # Desenha a barra de vida
        largura_vida = (self.jogador.vida / 100) * 194
        pygame.draw.rect(self.janela, color='#522900' , rect=(180, 620, 200, 30))
        pygame.draw.rect(self.janela, VERDE, (183, 623, largura_vida, 24))
        
        # Desenha o hud do jogador
        self.janela.blit(self.hud_jogador , (50,550))
        
        # Desenha a pontuação
        texto_pontuacao = self.fonte.render(f"PONTUAÇÃO: {self.pontuacao}", True, BRANCO)
        self.janela.blit(texto_pontuacao,(950,650))

        # Desenha a rodada
        texto_rodada = self.fonte.render(f"Rodada: {self.rodada_atual}", True, BRANCO)
        self.janela.blit(texto_rodada, (190, 650))

    def renderizar(self):
        self.janela.blit(self.fundo, (0, 0))
        self.todas_sprites.draw(self.janela)
        self.desenhar_hud()
        pygame.display.flip()

    def rodar(self):
        fps = pygame.time.Clock()
        while self.rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.jogador.atacar("esquerda", self.inimigos)
                    elif event.key == pygame.K_d:
                        self.jogador.atacar("direita", self.inimigos)
                    elif event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.jogador.pular()
                    if not self.jogador.no_chao:
                        if event.key == pygame.K_s:
                            self.jogador.smash(self.inimigos)

                        
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_spawn_time > self.intervalo_spawn:
                self.spawn_inimigo()
                self.ultimo_spawn_time = tempo_atual

            if self.pontuacao >= self.pontuacao_proxima_rodada:
                self.avancar_rodada()
            
            if self.jogador.vida <= 0:
                self.rodando = False

            self.renderizar()
            self.inimigos.update(self.jogador)
            self.jogador.update()
            fps.tick(FPS)