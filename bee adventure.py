import pygame, sys, random

# Função para desenhar o chão do jogo
def draw_floor():
    # Desenha o chão em duas posições para criar a ilusão de movimento
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

# Função para criar os canos e mel
def create_pipe():
    # Seleciona uma posição aleatória para os canos
    random_pipe_pos = random.choice(pipe_height)
    # Define o retângulo do cano inferior
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    # Define o retângulo do cano superior com deslocamento vertical
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))

    # Adiciona um item de mel ou pote de mel com probabilidades diferentes
    mel_type = random.choices(['mel', 'pote-mel'], weights=[95, 5], k=1)[0]
    if mel_type == 'mel':
        # Mel comum
        mel = mel_surface.get_rect(center=(700, random_pipe_pos - 150))
        mel_value = 1  # Valor do mel
    else:
        # Pote de mel (valor maior)
        mel = pote_mel_surface.get_rect(center=(700, random_pipe_pos - 150))
        mel_value = 5

    return bottom_pipe, top_pipe, (mel, mel_value)

# Função para mover os canos para a esquerda
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= ace  # Move o cano de acordo com a velocidade atual
    return pipes

# Função para desenhar os canos
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            # Desenha o cano normal se for inferior
            screen.blit(pipe_surface, pipe)
        else:
            # Desenha o cano invertido se for superior
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Função para remover canos que saíram da tela
def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -600:  # Verifica se o cano está fora da tela
            pipes.remove(pipe)
    return pipes

# Função para mover os itens de mel para a esquerda
def move_mels(mels):
    for mel_info in mels:
        mel, _ = mel_info
        mel.centerx -= ace  # Move o mel de acordo com a velocidade atual
    return mels

# Função para desenhar os itens de mel
def draw_mels(mels):
    for mel_info in mels:
        mel, mel_value = mel_info
        if mel_value == 1:
            # Desenha o mel comum
            screen.blit(mel_surface, mel)
        else:
            # Desenha o pote de mel
            screen.blit(pote_mel_surface, mel)

# Função para verificar colisão entre a abelha e os itens de mel
def check_mel_collision(mels):
    global score
    for mel_info in mels:
        mel, mel_value = mel_info
        if bird_rect.colliderect(mel):  # Detecta colisão
            score += mel_value  # Atualiza o placar
            score_sound.play()  # Toca o som de pontuação
            mels.remove(mel_info)  # Remove o item coletado
    return mels

# Função para verificar colisão entre a abelha e os canos ou limites da tela
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):  # Detecta colisão com o cano
            death_sound.play()  # Toca o som de morte
            return False

    # Verifica se a abelha bateu no topo ou no chão
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

# Função para rotacionar a abelha durante o voo
def rotate_bird(bird):
    # Rota a abelha com base no movimento vertical
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Função para alternar entre os frames da animação da abelha
def bird_animation():
    new_bird = bird_frames[bird_index]
    # Atualiza o retângulo da abelha para o novo frame
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

# Função para exibir o placar
def score_display(game_state):
    if game_state == 'main_game':
        # Exibe o placar atual
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        # Exibe o high score na tela de game over
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 600))
        screen.blit(high_score_surface, high_score_rect)

# Atualiza o high score se o placar atual for maior
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Função para aumentar a velocidade dos canos com base no placar
def update_speed(score):
    global ace
    ace = 4 + (score // 3)  # Incrementa a velocidade a cada 3 pontos

# Inicialização do pygame
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Variáveis do jogo
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
ace = 5  # Velocidade inicial
ticks = 120  # Taxa de atualização do jogo

# Carregando e redimensionando os elementos gráficos
bg_surface = pygame.image.load('background.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 1024))
floor_surface = pygame.image.load('base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Carregando e redimensionando a abelha
bird_downflap = pygame.transform.scale(pygame.image.load('abelha.png').convert_alpha(), (50, 50))
bird_midflap = pygame.transform.scale(pygame.image.load('abelha.png').convert_alpha(), (50, 50))
bird_upflap = pygame.transform.scale(pygame.image.load('abelha.png').convert_alpha(), (50, 50))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Carregando os canos
pipe_surface = pygame.image.load("pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Carregando os itens de mel
mel_surface = pygame.image.load('mel.png').convert_alpha()
mel_surface = pygame.transform.scale(mel_surface, (60, 70))
pote_mel_surface = pygame.image.load('pote-mel.png').convert_alpha()
pote_mel_surface = pygame.transform.scale(pote_mel_surface, (60, 70))
mel_list = []

# Tela de game over
game_over_surface = pygame.transform.scale(pygame.image.load('message.png').convert_alpha(), (576, 1024))
game_over_rect = game_over_surface.get_rect(center=(288, 512))

# Sons
flap_sound = pygame.mixer.Sound('sfx_wing.wav')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')

# Lista para controlar os canos já pontuados
scored_pipes = []

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8  # Impulso para cima
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                # Reinicia o jogo
                game_active = True
                pipe_list.clear()
                mel_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
                ace = 5
                scored_pipes.clear()

        if event.type == SPAWNPIPE:
            # Adiciona novos canos e mel ao jogo
            bottom_pipe, top_pipe, mel_info = create_pipe()
            pipe_list.extend([bottom_pipe, top_pipe])
            mel_list.append(mel_info)

        if event.type == BIRDFLAP:
            # Alterna entre os frames da abelha
            bird_index = (bird_index + 1) % 3
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))  # Desenha o fundo

    if game_active:
        # Lógica da abelha
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)  # Verifica colisões

        # Lógica dos canos
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Lógica do mel
        mel_list = move_mels(mel_list)
        mel_list = check_mel_collision(mel_list)
        draw_mels(mel_list)

        update_speed(score)  # Atualiza a velocidade com base no placar
        score_display('main_game')  # Exibe o placar

    else:
        # Tela de game over
        ace = 5  # Reinicia a velocidade
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)  # Atualiza o high score
        score_display('game_over')  # Exibe o high score

    # Lógica do chão
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(ticks)  # Controla a taxa de atualização do jogo
