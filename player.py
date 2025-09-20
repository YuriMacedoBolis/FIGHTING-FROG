import pygame
from funcoes import carregar_imagem , virar_imagem

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, jogo):
        super().__init__()
        self.x = x
        self.y = y
        self.largura, self.altura = 200, 200
        self.jogo = jogo
        self.direcao_visual = 'direita'
        self.vida = 100
        
        # ATAQUE
        self.esta_fazendo_smash = False
        self.esta_atacando = False
        self.tempo_ataque = 0
        self.duracao_ataque = 100

        # PULAR
        self.vel_y = 0
        self.gravidade = 1.4
        self.forca_pulo = -25
        self.no_chao = True
        self.estado = "idle"

        #SAPO_INICIAL
        self.image_inicial = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\Sapo_inicial.png", self.largura, self.altura)
        self.image_inicial_esq = virar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\Sapo_inicial.png", self.largura, self.altura)
        
        self.image = self.image_inicial
        self.rect = self.image_inicial.get_rect(center=(x, y))

        #SAPO_SOCO_DIREITA
        self.image_sapo_ataque = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\Sapo_ataque2.png", self.largura + 20, self.altura)

        #SAPO_SOCO_ESQUERDA
        self.image_sapo_ataque_esq = virar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\Sapo_ataque2.png" , self.largura +20, self.altura)

        #SAPO_PULANDO_DIREITA
        self.image_sapo_pulo = carregar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\sapo_pulando.png" , self.largura , self.altura)

        #SAPO_PULANDO_ESQUERDA
        self.image_sapo_pulo_esq = virar_imagem("PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\sapo_pulando.png" , self.largura , self.altura)

        #SAPO SMASH 
        self.image_sapo_caindo = carregar_imagem('PROJETO_JOGO\\IMAGENS PISKEL\\Sapo\\sapo caindo.png' , self.largura , self.altura)

        
    def update(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.vel_y = 0
            self.no_chao = True
            if self.esta_fazendo_smash:
                self.esta_fazendo_smash = False
                self.image = self.image_inicial
    
        if self.esta_atacando:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ataque > self.duracao_ataque:
                self.esta_atacando = False
                
                if self.direcao_visual == "direita":
                    self.image = self.image_inicial
                else:
                    self.image = self.image_inicial_esq
    

        if self.esta_atacando:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ataque > self.duracao_ataque:
                self.esta_atacando = False
                self.image = self.image_inicial
                

    def smash(self, inimigos):
        if not  self.esta_fazendo_smash:
            smash_hitbox = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, self.rect.height)
            self.esta_fazendo_smash = True
            self.tempo_ataque = pygame.time.get_ticks()
            self.image = self.image_sapo_caindo
            self.vel_y = 20 

            for inimigo in inimigos:
                if smash_hitbox.colliderect(inimigo.rect):
                    inimigo.vida -= 50
                    if inimigo.vida <= 0:
                        self.jogo.pontuacao += 1
                        inimigo.kill()
        
        if self.no_chao:
            self.esta_fazendo_smash = False

    def atacar(self, direcao, inimigos):
        if not self.esta_atacando:
            self.esta_atacando = True
            self.tempo_ataque = pygame.time.get_ticks()
            self.direcao_visual = direcao
            
            if self.no_chao:
                if direcao == "esquerda":
                    hitbox = pygame.Rect(self.rect.left - 40, self.rect.top, 40, self.rect.height)
                    self.image = self.image_sapo_ataque_esq
                elif direcao == "direita":
                    hitbox = pygame.Rect(self.rect.right, self.rect.top, 40, self.rect.height)
                    self.image = self.image_sapo_ataque
                    
                else:
                    hitbox = None
                
            else:
                if direcao == "esquerda":
                    hitbox = pygame.Rect(self.rect.left - 40, self.rect.top, 40, self.rect.height)
                    self.image = self.image_sapo_pulo_esq
                elif direcao == "direita":
                    hitbox = pygame.Rect(self.rect.right, self.rect.top, 40, self.rect.height)
                    self.image = self.image_sapo_pulo

            

            if hitbox:
                for inimigo in inimigos:
                    if hitbox.colliderect(inimigo.rect):
                        inimigo.vida -= 25
                        if inimigo.vida <= 0:
                            self.jogo.pontuacao += 1
                            inimigo.kill()

    def pular(self):
        if self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False