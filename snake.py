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

class TipoEfeitoComida(Enum):
    CRESCIMENTO = 1
    IMUNIDADE = 2
    VIDA_EXTRA = 3
    TAMANHO_GRANDE = 4
    VELOCIDADE = 5
    REDUCAO = 6

@dataclass
class ComidaEspecial:
    tipo: TipoEfeitoComida
    posicao: Tuple[int, int]
    cor: Tuple[int, int, int]
    tempo_criacao: float
    duracao: float  
    
    def expirou(self) -> bool:
        return time() > self.tempo_criacao + self.duracao

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
        self.largura = 1
        self.velocidade = 1  
        self.tempo_velocidade = 0
        self.atualizacoes_movimento = 0  

    def mover(self):
        if not self.vivo:
            return
        
        
        self.atualizacoes_movimento += self.velocidade
        if self.atualizacoes_movimento < 1:
            return
        
        self.atualizacoes_movimento = 0
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
        if self.velocidade > 1 and tempo_atual > self.tempo_velocidade:
            self.velocidade = 1

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

    def reduzir_tamanho(self):
        tamanho_atual = len(self.corpo)
        if tamanho_atual <= 1:
            self.vivo = False
            return False
        
        novo_tamanho = max(1, tamanho_atual // 2)
        self.corpo = self.corpo[:novo_tamanho]
        return True

class Jogo:
    def __init__(self, num_jogadores: int):
        self.tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
        pygame.display.set_caption("Jogo da Cobra Multiplayer")
        self.relogio = pygame.time.Clock()
        self.num_jogadores = num_jogadores
        
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
        self.comidas_especiais = []
        self.ultimo_comida_especial = time()
        self.intervalo_comida_especial = 10
        
        for _ in range(num_jogadores):
            self.gerar_nova_comida()

    def gerar_nova_comida(self) -> bool:
        """Gera uma nova comida em uma posição aleatória livre. Retorna True se conseguiu gerar."""
        posicoes_ocupadas = self.obter_posicoes_ocupadas()
        tentativas = 0
        max_tentativas = 100
        
        while tentativas < max_tentativas:
            pos = (random.randint(0, CONTAGEM_GRADE-1), random.randint(0, CONTAGEM_GRADE-1))
            if pos not in posicoes_ocupadas:
                self.comidas.append(pos)
                return True
            tentativas += 1
        return False

    def gerar_comida_especial(self):
        tempo_atual = time()
        if tempo_atual - self.ultimo_comida_especial < self.intervalo_comida_especial:
            return
        if random.random() < 0.2: 
            posicoes_ocupadas = self.obter_posicoes_ocupadas()
            tentativas = 0
            max_tentativas = 100
            
            while tentativas < max_tentativas:
                pos = (random.randint(0, CONTAGEM_GRADE-1), random.randint(0, CONTAGEM_GRADE-1))
                if pos not in posicoes_ocupadas:
                    tipo = random.choice(list(TipoEfeitoComida))
                    cores_comida_especial = {
                        TipoEfeitoComida.CRESCIMENTO: (255, 0, 255),
                        TipoEfeitoComida.IMUNIDADE: (0, 255, 255),
                        TipoEfeitoComida.VIDA_EXTRA: (255, 215, 0),
                        TipoEfeitoComida.TAMANHO_GRANDE: (255, 69, 0),
                        TipoEfeitoComida.VELOCIDADE: (50, 205, 50), 
                        TipoEfeitoComida.REDUCAO: (139, 0, 0)
                    }
                    
                    duracoes_comida_especial = {
                        TipoEfeitoComida.CRESCIMENTO: 8,
                        TipoEfeitoComida.IMUNIDADE: 6,
                        TipoEfeitoComida.VIDA_EXTRA: 10,
                        TipoEfeitoComida.TAMANHO_GRANDE: 8,
                        TipoEfeitoComida.VELOCIDADE: 5,
                        TipoEfeitoComida.REDUCAO: 15
                    }
                    
                    self.comidas_especiais.append(ComidaEspecial(
                        tipo=tipo,
                        posicao=pos,
                        cor=cores_comida_especial[tipo],
                        tempo_criacao=tempo_atual,
                        duracao=duracoes_comida_especial[tipo]
                    ))
                    self.ultimo_comida_especial = tempo_atual
                    break
                tentativas += 1

    def obter_posicoes_ocupadas(self) -> set:
        ocupadas = set()
        for cobra in self.cobras:
            if cobra.vivo:
                ocupadas.update(cobra.corpo)
        ocupadas.update(self.comidas)
        ocupadas.update(p.posicao for p in self.comidas_especiais)
        return ocupadas

    def atualizar_comidas_especiais(self):
        """Remove comidas especiais expiradas"""
        self.comidas_especiais = [p for p in self.comidas_especiais if not p.expirou()]

    def verificar_colisoes(self):
        for i, cobra in enumerate(self.cobras):
            if not cobra.vivo:
                continue
            cabeca = cobra.corpo[0]
            
            if cabeca in self.comidas:
                self.comidas.remove(cabeca)
                cobra.crescimento_pendente += 1
                self.gerar_nova_comida()

            for comida_especial in self.comidas_especiais[:]:
                if cabeca == comida_especial.posicao:
                    self.comidas_especiais.remove(comida_especial)
                    tempo_atual = time()
                    
                    if comida_especial.tipo == TipoEfeitoComida.CRESCIMENTO:
                        cobra.crescimento_pendente += 3
                    elif comida_especial.tipo == TipoEfeitoComida.IMUNIDADE:
                        cobra.imune = True
                        cobra.tempo_imunidade = tempo_atual + 5
                    elif comida_especial.tipo == TipoEfeitoComida.VIDA_EXTRA:
                        cobra.vidas_extras += 1
                    elif comida_especial.tipo == TipoEfeitoComida.TAMANHO_GRANDE:
                        cobra.tamanho_grande = True
                        cobra.largura = 2
                        cobra.tempo_tamanho_grande = tempo_atual + 7
                    elif comida_especial.tipo == TipoEfeitoComida.VELOCIDADE:
                        cobra.velocidade = 1.5
                        cobra.tempo_velocidade = tempo_atual + 5
                    elif comida_especial.tipo == TipoEfeitoComida.REDUCAO:
                        if not cobra.reduzir_tamanho():
                            print(f"Jogador {i+1} foi eliminado por ficar muito pequeno!")
            
            for j, outra_cobra in enumerate(self.cobras):
                if not outra_cobra.vivo or i == j:
                    continue
                if cabeca in outra_cobra.corpo:
                    if cobra.imune:
                        continue
                    else:
                        if cobra.vidas_extras > 0:
                            cobra.vidas_extras -= 1
                        else:
                            cobra.vivo = False
                        break

            if len(cobra.corpo) > 1 and cabeca in cobra.corpo[1:]:
                if cobra.imune:
                    continue
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
        
        for comida_especial in self.comidas_especiais:
            pygame.draw.rect(self.tela, comida_especial.cor,
                           (comida_especial.posicao[0] * TAMANHO_GRADE,
                            comida_especial.posicao[1] * TAMANHO_GRADE,
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
            
            self.gerar_comida_especial()
            self.atualizar_comidas_especiais()

            self.desenhar()
            self.relogio.tick(10)

if __name__ == "__main__":
    NUM_JOGADORES = 2
    jogo = Jogo(NUM_JOGADORES)
    jogo.executar()
