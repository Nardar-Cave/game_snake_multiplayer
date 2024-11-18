import pygame
import random
import sys
from typing import List, Tuple
from enum import Enum
from dataclasses import dataclass
from time import time

pygame.init()

TAMANHO_JANELA = 800
TAMANHO_GRADE = 20
CONTAGEM_GRADE = TAMANHO_JANELA // TAMANHO_GRADE
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CORES = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)] 
COR_COMIDA = (255, 165, 0)
COR_COMIDA_ESPECIAL = (255, 0, 255)

class TipoPowerUp(Enum):
    CRESCIMENTO = 1
    IMUNIDADE = 2
    VIDA_EXTRA = 3
    EMPURRAR = 4
    TAMANHO_GRANDE = 5

@dataclass
class PowerUp:
    tipo: TipoPowerUp
    posicao: Tuple[int, int]
    cor: Tuple[int, int, int]

class Cobra:
    def __init__(self, pos: Tuple[int, int], cor: Tuple[int, int, int], controles: Tuple[int, int, int, int]):
        self.corpo = [pos]
        self.direcao = [1, 0]
        self.cor = cor
        self.controles = controles
        self.vivo = True
        self.crescimento_pendente = 0
        self.imune = False
        self.tempo_imunidade = 0
        self.tamanho_grande = False
        self.tempo_tamanho_grande = 0
        self.vidas_extras = 0
        self.pode_empurrar = False
        self.tempo_empurrar = 0
        self.largura = 1 

    def mover(self):
        if not self.vivo:
            return

        nova_cabeca = (
            (self.corpo[0][0] + self.direcao[0]) % CONTAGEM_GRADE,
            (self.corpo[0][1] + self.direcao[1]) % CONTAGEM_GRADE
        )
        self.corpo.insert(0, nova_cabeca)
        
        if self.crescimento_pendente > 0:
            self.crescimento_pendente -= 1
        else:
            self.corpo.pop()


        tempo_atual = time()
        if self.imune and tempo_atual > self.tempo_imunidade:
            self.imune = False
        if self.tamanho_grande and tempo_atual > self.tempo_tamanho_grande:
            self.tamanho_grande = False
            self.largura = 1
        if self.pode_empurrar and tempo_atual > self.tempo_empurrar:
            self.pode_empurrar = False

    def processar_entrada(self, teclas):
        if not self.vivo:
            return

        cima, baixo, esquerda, direita = self.controles
        if teclas[cima] and self.direcao != [0, 1]:
            self.direcao = [0, -1]
        elif teclas[baixo] and self.direcao != [0, -1]:
            self.direcao = [0, 1]
        elif teclas[esquerda] and self.direcao != [1, 0]:
            self.direcao = [-1, 0]
        elif teclas[direita] and self.direcao != [-1, 0]:
            self.direcao = [1, 0]

class Jogo:
    def __init__(self, num_jogadores: int):
        self.tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
        pygame.display.set_caption("Jogo da Cobra Multiplayer")
        self.relogio = pygame.time.Clock()
        
        controles = [
            (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
            (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
            (pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l),
            (pygame.K_t, pygame.K_g, pygame.K_f, pygame.K_h)
        ]
        
        self.cobras = []
        posicoes_iniciais = [
            (5, 5), (CONTAGEM_GRADE-6, CONTAGEM_GRADE-6),
            (5, CONTAGEM_GRADE-6), (CONTAGEM_GRADE-6, 5)
        ]
        
        for i in range(num_jogadores):
            self.cobras.append(Cobra(posicoes_iniciais[i], CORES[i], controles[i]))
        
        self.comidas = []
        self.power_ups = []
        self.gerar_comidas(num_jogadores)

    def gerar_power_up(self):
        if random.random() < 0.05:  
            posicoes_ocupadas = self.obter_posicoes_ocupadas()
            while True:
                pos = (random.randint(0, CONTAGEM_GRADE-1), random.randint(0, CONTAGEM_GRADE-1))
                if pos not in posicoes_ocupadas:
                    tipo = random.choice(list(TipoPowerUp))
                    cores_power_ups = {
                        TipoPowerUp.CRESCIMENTO: (255, 0, 255),
                        TipoPowerUp.IMUNIDADE: (0, 255, 255),
                        TipoPowerUp.VIDA_EXTRA: (255, 215, 0),
                        TipoPowerUp.EMPURRAR: (128, 0, 128),
                        TipoPowerUp.TAMANHO_GRANDE: (255, 69, 0)
                    }
                    self.power_ups.append(PowerUp(tipo, pos, cores_power_ups[tipo]))
                    break

    def gerar_comidas(self, contagem: int):
        self.comidas = []
        posicoes_ocupadas = self.obter_posicoes_ocupadas()
        
        for _ in range(contagem):
            while True:
                pos = (random.randint(0, CONTAGEM_GRADE-1), random.randint(0, CONTAGEM_GRADE-1))
                if pos not in posicoes_ocupadas:
                    self.comidas.append(pos)
                    posicoes_ocupadas.add(pos)
                    break
        
        self.gerar_power_up()

    def obter_posicoes_ocupadas(self) -> set:
        ocupadas = set()
        for cobra in self.cobras:
            if cobra.vivo:
                ocupadas.update(cobra.corpo)
        ocupadas.update(self.comidas)
        ocupadas.update(p.posicao for p in self.power_ups)
        return ocupadas

    def empurrar_cobra(self, cobra_empurradora, cobra_empurrada):
        direcao = cobra_empurradora.direcao
        cabeca_empurrada = cobra_empurrada.corpo[0]
        nova_posicao = (
            (cabeca_empurrada[0] + direcao[0]) % CONTAGEM_GRADE,
            (cabeca_empurrada[1] + direcao[1]) % CONTAGEM_GRADE
        )
        cobra_empurrada.corpo.insert(0, nova_posicao)
        cobra_empurrada.corpo.pop()

    def verificar_colisoes(self):
        for i, cobra in enumerate(self.cobras):
            if not cobra.vivo:
                continue

            cabeca = cobra.corpo[0]
            

            if cabeca in self.comidas:
                self.comidas.remove(cabeca)
                cobra.crescimento_pendente += 1
                if len(self.comidas) < len([c for c in self.cobras if c.vivo]):
                    self.gerar_comidas(len([c for c in self.cobras if c.vivo]))


            for power_up in self.power_ups[:]:
                if cabeca == power_up.posicao:
                    self.power_ups.remove(power_up)
                    tempo_atual = time()
                    
                    if power_up.tipo == TipoPowerUp.CRESCIMENTO:
                        cobra.crescimento_pendente += 3
                    elif power_up.tipo == TipoPowerUp.IMUNIDADE:
                        cobra.imune = True
                        cobra.tempo_imunidade = tempo_atual + 5 
                    elif power_up.tipo == TipoPowerUp.VIDA_EXTRA:
                        cobra.vidas_extras += 1
                    elif power_up.tipo == TipoPowerUp.EMPURRAR:
                        cobra.pode_empurrar = True
                        cobra.tempo_empurrar = tempo_atual + 10  
                    elif power_up.tipo == TipoPowerUp.TAMANHO_GRANDE:
                        cobra.tamanho_grande = True
                        cobra.largura = 2
                        cobra.tempo_tamanho_grande = tempo_atual + 7  
            

            for j, outra_cobra in enumerate(self.cobras):
                if not outra_cobra.vivo or i == j:
                    continue


                if cabeca in outra_cobra.corpo:
                    if cobra.imune:
                        continue  
                    elif cobra.pode_empurrar:
                        self.empurrar_cobra(cobra, outra_cobra)
                    else:
                        if cobra.vidas_extras > 0:
                            cobra.vidas_extras -= 1
                        else:
                            cobra.vivo = False
                        break

    def desenhar(self):
        self.tela.fill(PRETO)
        
        for comida in self.comidas:
            pygame.draw.rect(self.tela, COR_COMIDA,
                           (comida[0] * TAMANHO_GRADE, comida[1] * TAMANHO_GRADE, 
                            TAMANHO_GRADE, TAMANHO_GRADE))
        
        for power_up in self.power_ups:
            pygame.draw.rect(self.tela, power_up.cor,
                           (power_up.posicao[0] * TAMANHO_GRADE, 
                            power_up.posicao[1] * TAMANHO_GRADE,
                            TAMANHO_GRADE, TAMANHO_GRADE))
        
        for cobra in self.cobras:
            if cobra.vivo:
                cor = cobra.cor
                if cobra.imune:
                    cor = (cor[0], min(255, cor[1] + 100), min(255, cor[2] + 100))
                
                for segmento in cobra.corpo:
                    largura_pixels = TAMANHO_GRADE * cobra.largura
                    offset = (cobra.largura - 1) * TAMANHO_GRADE // 2
                    
                    pygame.draw.rect(self.tela, cor,
                                   (segmento[0] * TAMANHO_GRADE - offset, 
                                    segmento[1] * TAMANHO_GRADE - offset,
                                    largura_pixels, largura_pixels))
        
        pygame.display.flip()

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            teclas = pygame.key.get_pressed()
            for cobra in self.cobras:
                cobra.processar_entrada(teclas)
            
            for cobra in self.cobras:
                cobra.mover()
            
            self.verificar_colisoes()
            
            cobras_vivas = [cobra for cobra in self.cobras if cobra.vivo]
            if len(cobras_vivas) <= 1:
                vencedor = cobras_vivas[0] if cobras_vivas else None
                print(f"Jogo terminado! {'Jogador ' + str(self.cobras.index(vencedor) + 1) + ' venceu!' if vencedor else 'Empate!'}")
                pygame.quit()
                sys.exit()
            
            self.desenhar()
            self.relogio.tick(10)

if __name__ == "__main__":
    NUM_JOGADORES = 2  
    jogo = Jogo(NUM_JOGADORES)
    jogo.executar()
