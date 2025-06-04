import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configuração da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Meu Jogo de Futebol")

# Cores
VERDE = (0, 128, 0) # Cor do campo
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Posição e tamanhos iniciais
bola_pos = [LARGURA_TELA // 2, ALTURA_TELA - 100]
bola_raio = 15
bola_vel = [0, 0] # Velocidade inicial da bola (não se move até ser chutada)

goleiro_largura = 80
goleiro_altura = 20

# Posição do gol primeiro, pois o goleiro será baseado nela
gol_largura = 200
gol_altura = 10
gol_pos = [LARGURA_TELA // 2 - gol_largura // 2, 80] # Posição do gol

# O goleiro será posicionado logo acima ou dentro do gol
# Para ficar na frente do gol, vamos ajustar o Y do goleiro
# Queremos que a base do goleiro (goleiro_pos[1] + goleiro_altura)
# esteja alinhada com a base do gol (gol_pos[1] + gol_altura)
goleiro_pos = [LARGURA_TELA // 2 - goleiro_largura // 2, gol_pos[1] + gol_altura - goleiro_altura]
goleiro_vel_x = 3 # Velocidade do goleiro

jogador_pos = [LARGURA_TELA // 2, ALTURA_TELA - 50]
jogador_tamanho = 30

# Placar
gols = 0
defesas = 0
fonte = pygame.font.Font(None, 36) # Fonte para o placar

# Estado do jogo
bola_chutada = False
alvo_chute = None # Onde a bola vai mirar ao ser chutada

def reset_rodada():
    global bola_pos, bola_vel, bola_chutada, alvo_chute, goleiro_pos
    bola_pos = [LARGURA_TELA // 2, ALTURA_TELA - 100]
    bola_vel = [0, 0]
    bola_chutada = False
    alvo_chute = None
    # Resetar a posição horizontal do goleiro para o centro do gol para cada nova rodada
    goleiro_pos[0] = LARGURA_TELA // 2 - goleiro_largura // 2

# --- Loop principal do jogo ---
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and not bola_chutada:
            # O jogador clica para chutar
            alvo_chute = evento.pos
            # Calcula a velocidade da bola para ir em direção ao alvo
            dx = alvo_chute[0] - bola_pos[0]
            dy = alvo_chute[1] - bola_pos[1]
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                velocidade_chute = 10 # Ajuste a velocidade do chute
                bola_vel[0] = (dx / dist) * velocidade_chute
                bola_vel[1] = (dy / dist) * velocidade_chute
                bola_chutada = True

    # Atualiza a posição do goleiro
    goleiro_pos[0] += goleiro_vel_x
    if goleiro_pos[0] <= gol_pos[0] or goleiro_pos[0] + goleiro_largura >= gol_pos[0] + gol_largura:
        goleiro_vel_x *= -1 # Inverte a direção

    # Atualiza a posição da bola se ela foi chutada
    if bola_chutada:
        bola_pos[0] += bola_vel[0]
        bola_pos[1] += bola_vel[1]

        # Verifica colisão com o goleiro
        if (bola_pos[0] + bola_raio > goleiro_pos[0] and
            bola_pos[0] - bola_raio < goleiro_pos[0] + goleiro_largura and
            bola_pos[1] + bola_raio > goleiro_pos[1] and
            bola_pos[1] - bola_raio < goleiro_pos[1] + goleiro_altura):
            defesas += 1
            reset_rodada()

        # Verifica se a bola passou pelo goleiro e está na área do gol
        # Importante: Se a bola já foi "defendida" acima, esta condição não será atingida.
        # Ela verifica se a bola está dentro da área do gol E não colidiu com o goleiro.
        if (bola_pos[1] - bola_raio < gol_pos[1] + gol_altura and # A bola passou pela linha do gol verticalmente
            bola_pos[0] + bola_raio > gol_pos[0] and # A bola está entre as laterais do gol
            bola_pos[0] - bola_raio < gol_pos[0] + gol_largura and
            not pygame.Rect(goleiro_pos[0], goleiro_pos[1], goleiro_largura, goleiro_altura).colliderect(
                pygame.Rect(bola_pos[0] - bola_raio, bola_pos[1] - bola_raio, bola_raio * 2, bola_raio * 2)
            )):
            gols += 1
            reset_rodada()

        # Se a bola sair da tela por cima, ou muito para os lados (fora do gol)
        # Ajustei a condição para verificar se a bola passou do gol em Y ou saiu das laterais da tela
        if bola_pos[1] < (gol_pos[1] - bola_raio) or bola_pos[0] < 0 or bola_pos[0] > LARGURA_TELA:
            reset_rodada()

    # Desenha na tela
    TELA.fill(VERDE) # Campo de futebol

    # Desenha o gol
    pygame.draw.rect(TELA, BRANCO, (gol_pos[0], gol_pos[1], gol_largura, gol_altura), 2) # Desenha apenas o contorno

    # Desenha o goleiro
    pygame.draw.rect(TELA, AZUL, (goleiro_pos[0], goleiro_pos[1], goleiro_largura, goleiro_altura))

    # Desenha o jogador (um círculo para simplificar)
    pygame.draw.circle(TELA, VERMELHO, (int(jogador_pos[0]), int(jogador_pos[1])), jogador_tamanho)

    # Desenha a bola
    pygame.draw.circle(TELA, PRETO, (int(bola_pos[0]), int(bola_pos[1])), bola_raio)

    # Desenha o placar
    texto_gols = fonte.render(f"Gols: {gols}", True, BRANCO)
    texto_defesas = fonte.render(f"Defesas: {defesas}", True, BRANCO)
    TELA.blit(texto_gols, (10, 10))
    TELA.blit(texto_defesas, (10, 50))

    # Atualiza a tela
    pygame.display.flip()

    # Controle de FPS
    pygame.time.Clock().tick(60) # 60 frames por segundo

pygame.quit()
sys.exit()