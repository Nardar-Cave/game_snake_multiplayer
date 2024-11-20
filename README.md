# 🐍 Jogo da Cobra Multijogador (Local)

## Descrição do Projeto

Este é um jogo da cobra multiplayer (local) desenvolvido em Python utilizando a biblioteca Pygame. O jogo permite que até 4 jogadores (local) compitam simultaneamente em um grid, controlando suas próprias cobras, coletando comidas e tentando sobreviver.

## 🎮 Características Principais

- Suporte para 2-4 jogadores (local)
- Sistema de comidas especiais com efeitos únicos
- Mecânicas de jogo dinâmicas
- Controles personalizados para cada jogador
- Sistema de vidas extras
- Efeitos especiais como imunidade e crescimento

## 🕹️ Controles

### Jogador 1 (Verde)
- Cima: W
- Baixo: S
- Esquerda: A
- Direita: D

### Jogador 2 (Vermelho)
- Cima: Seta para cima
- Baixo: Seta para baixo
- Esquerda: Seta para esquerda
- Direita: Seta para direita

### Jogador 3 (Azul)
- Cima: I
- Baixo: K
- Esquerda: J
- Direita: L

### Jogador 4 (Amarelo)
- Cima: T
- Baixo: G
- Esquerda: F
- Direita: H

## 🍎 Comidas Especiais

### Tipos de Comidas e Efeitos

| Comida | Cor | Efeito | Duração |
|--------|-----|--------|---------|
| Crescimento | Magenta | Adiciona 3 segmentos à cobra | 8 segundos |
| Imunidade | Ciano | Torna a cobra temporariamente imune | 6 segundos |
| Vida Extra | Dourado | Adiciona uma vida extra | Permanente |
| Tamanho Grande | Laranja | Aumenta a largura da cobra | 8 segundos |
| Velocidade | Verde Lima | Aumenta a velocidade em 50% | 5 segundos |
| Redução | Vermelho Escuro | Reduz o tamanho da cobra pela metade | 15 segundos |

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.7+
- Pygame

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/Nardar-Cave/game_snake_multiplayer.git
cd multiplayer-snake-game
```

2. Instale as dependências:
```bash
pip install pygame
```

3. Execute o jogo:
```bash
python snake_game.py
```

### Alterando o Número de Jogadores
No arquivo `snake_game.py`, modifique a variável `NUM_JOGADORES` na linha final. Valores suportados: 2-4.

```python
NUM_JOGADORES = 2  # Altere para 3 ou 4 conforme desejado
```

## 🚀 Pontos Positivos
- Multiplayer divertido
- Mecânicas de jogo variadas
- Comidas especiais com efeitos interessantes
- Fácil de expandir e personalizar

## 🛠️ Pontos a Melhorar
- Adicionar menu inicial
- Implementar sistema de pontuação
- Criar tela de game over mais elaborada
- Adicionar efeitos sonoros
- Suportar configurações personalizadas

## 🤝 Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 🎨 Créditos
Desenvolvido como um projeto de estudo da biblioteca Pygame.
