import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))

    # Randomização do tipo de mel (5% pote-mel e 95% mel comum)
    mel_type = random.choices(['mel', 'pote-mel'], weights=[95, 5], k=1)[0]
    if mel_type == 'mel':
        mel = mel_surface.get_rect(center=(700, random_pipe_pos - 150))
        mel_value = 1
    else:
        mel = pote_mel_surface.get_rect(center=(700, random_pipe_pos - 150))
        mel_value = 5

    return bottom_pipe, top_pipe, (mel, mel_value)

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= ace
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -600:
            pipes.remove(pipe)
    return pipes

def move_mels(mels):
    for mel_info in mels:
        mel, _ = mel_info
        mel.centerx -= ace
    return mels

def draw_mels(mels):
    for mel_info in mels:
        mel, mel_value = mel_info
        if mel_value == 1:
            screen.blit(mel_surface, mel)
        else:
            screen.blit(pote_mel_surface, mel)

def check_mel_collision(mels):
    global score
    for mel_info in mels:
        mel, mel_value = mel_info
        if bird_rect.colliderect(mel):
            score += mel_value
            score_sound.play()
            mels.remove(mel_info)
    return mels

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        # Exibir apenas o high_score na tela de game over
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 600))  # Ajuste de posição conforme necessário
        screen.blit(high_score_surface, high_score_rect)


        # Ajuste a posição para mais alto
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 600))  # Ajuste de 850 para 600
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Função para aumentar a velocidade com base no score, mas manter a criação de canos constante
def update_speed(score):
    global ace
    ace = 4 + (score // 3)  # Aumenta a velocidade dos canos de acordo com o score

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
ace = 5
ticks = 120

# Redimensionar o fundo de acordo com o tamanho da tela
bg_surface = pygame.image.load('background.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 1024))  # Redimensiona o fundo para o tamanho da tela

floor_surface = pygame.image.load('base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Redimensionar a abelha para um tamanho menor
bird_downflap = pygame.transform.scale2x(pygame.image.load('abelha.png').convert_alpha())
bird_downflap = pygame.transform.scale(bird_downflap, (50, 50))  # Redimensiona a abelha para 50x50
bird_midflap = pygame.transform.scale2x(pygame.image.load('abelha.png').convert_alpha())
bird_midflap = pygame.transform.scale(bird_midflap, (50, 50))  # Redimensiona a abelha para 50x50
bird_upflap = pygame.transform.scale2x(pygame.image.load('abelha.png').convert_alpha())
bird_upflap = pygame.transform.scale(bird_upflap, (50, 50))  # Redimensiona a abelha para 50x50

# Atualizando a lista de frames
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

# Mel e pote-mel (moedas) - Redimensionamento
mel_surface = pygame.image.load('mel.png').convert_alpha()
mel_surface = pygame.transform.scale(mel_surface, (60, 70))  # Redimensiona o mel
pote_mel_surface = pygame.image.load('pote-mel.png').convert_alpha()
pote_mel_surface = pygame.transform.scale(pote_mel_surface, (60, 70))  # Redimensiona o pote-mel
mel_list = []

game_over_surface = pygame.transform.scale2x(pygame.image.load('message.png').convert_alpha())
game_over_surface = pygame.transform.scale(game_over_surface, (576, 1024))
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('sfx_wing.wav')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')

# Lista de pipes que já pontuaram
scored_pipes = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                mel_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
                ace = 5
                scored_pipes.clear()

        if event.type == SPAWNPIPE:
            bottom_pipe, top_pipe, mel_info = create_pipe()
            pipe_list.extend([bottom_pipe, top_pipe])
            mel_list.append(mel_info)  # Adiciona o mel junto com seu valor

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Mel
        mel_list = move_mels(mel_list)
        mel_list = check_mel_collision(mel_list)
        draw_mels(mel_list)

        # Aumenta a velocidade conforme o score, mantendo o spawn das pipes constante
        update_speed(score)

        score_display('main_game')

    else:
        ace = 5
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(ticks)
