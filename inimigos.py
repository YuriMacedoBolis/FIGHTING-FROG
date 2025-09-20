import pygame
from funcoes import carregar_imagem, virar_imagem

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, vida , direcao_inicial):
        super().__init__()

        self.imagens_direitas = [
            carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Mosca\\mosca.png", 100, 100),
            carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Mosca\\mosca.2.png", 100, 100)
        ]
        self.imagens_esquerdas = [
            virar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Mosca\\mosca.png", 100, 100),
            virar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Mosca\\mosca.2.png", 100, 100)
        ]
        
        self.direcao_movimento = 1 if direcao_inicial == "direita" else -1
        self.direcao_visual = direcao_inicial
        self.image = self.imagens_direitas[0] if self.direcao_visual == "direita" else self.imagens_esquerdas[0]
        self.rect = self.image.get_rect(center=(x, y))

        # ANIMAÇÃO DAS ASAS
        self.frame_atual = 0
        self.ultimo_frame_time = pygame.time.get_ticks()
        self.intervalo_animacao = 150

        self.velocidade = velocidade
        self.vida = vida

        # ATAQUE INIMIGO
        self.tempo_ultimo_dano = pygame.time.get_ticks()
        self.cooldown_ataque = 350
        self.tempo_colisao = None

    def animar_asas(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_frame_time > self.intervalo_animacao:
            self.ultimo_frame_time = tempo_atual
            self.frame_atual = (self.frame_atual + 1) % len(self.imagens_direitas)
            
            if self.direcao_visual == "direita":
                self.image = self.imagens_direitas[self.frame_atual]
            else:
                self.image = self.imagens_esquerdas[self.frame_atual]

    def update(self, jogador):
        self.animar_asas()

        if self.rect.x < jogador.rect.x:
            self.direcao_visual = "direita"
        else:
            self.direcao_visual = "esquerda"

        if not self.rect.colliderect(jogador.rect):
            if self.direcao_visual == "direita":
                self.rect.x += self.velocidade
            else:
                self.rect.x -= self.velocidade
            self.tempo_colisao = None  
        else:
            self.atacar_jogador(jogador)

    def atacar_jogador(self, jogador):
        tempo_atual = pygame.time.get_ticks()
        if self.tempo_colisao is None:
            self.tempo_colisao = tempo_atual
            
        if (tempo_atual - self.tempo_colisao) > self.cooldown_ataque:
            jogador.vida -= 10
            self.tempo_colisao = tempo_atual