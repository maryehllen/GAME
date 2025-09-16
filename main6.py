import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da janela padrão
WIDTH, HEIGHT = 720, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Mover Imagem com Setas")

# Definindo a cor de fundo (usada se não houver imagem de fundo)
BG_COLOR = (193, 0, 40)  # cor de fundo (um tom escuro)

# Carregar a imagem do personagem principal (jogador)
image_file = "GAME/player.png"  # Coloque o nome correto da sua imagem aqui
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()  # Carregar a imagem
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centraliza a imagem
else:
    print("Imagem do personagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)  # Retângulo padrão para evitar erro

# Carregar a imagem do personagem alvo (para ser chutado)
target_file = "GAME/patrick.png"  # Você deve ter uma imagem para o alvo
if os.path.exists(target_file):
    target_img = pygame.image.load(target_file).convert_alpha()
    target_rect = target_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))  # Posição inicial ao lado do jogador
else:
    print("Imagem do personagem alvo não encontrada!")
    target_img = None
    target_rect = pygame.Rect(WIDTH // 2 + 200, HEIGHT // 2, 50, 50)

# Carregar a imagem de fundo (original)
background_file = "GAME/background.png"  # Caminho para sua imagem de fundo
if os.path.exists(background_file):
    background_orig = pygame.image.load(background_file).convert()
    background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
else:
    background_orig = None
    background = None
    print("Imagem de fundo não encontrada!")

# Velocidade de movimento do jogador
SPEED = 3  # pixels por movimento
JUMP_STRENGTH = 18  # Força do pulo (quanto maior, mais alto o pulo)
GRAVITY = 0.3  # Gravidade, fazendo o personagem cair
JUMPING = False  # Indica se o personagem está no ar
VELOCITY_Y = 0  # Velocidade no eixo Y do jogador

# Variáveis para o alvo chutado
target_velocity_x = 0
target_velocity_y = 0
target_jumping = False  # Se o alvo está no ar (foi chutado)
target_gravity = GRAVITY

# Função para centralizar a imagem conforme o tamanho da tela
def centralize_image():
    global img_rect, WIDTH, HEIGHT
    img_rect.center = (WIDTH // 2, HEIGHT // 2)

# Controle redimensionamento
last_width, last_height = WIDTH, HEIGHT

# Limitar movimento para não sair da tela (funciona para ambos)
def limit_movement(rect):
    if rect.left < 0:
        rect.left = 0
    if rect.right > WIDTH:
        rect.right = WIDTH
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > HEIGHT:
        rect.bottom = HEIGHT

# Função para pular do jogador
def jump():
    global VELOCITY_Y, JUMPING
    if not JUMPING:
        VELOCITY_Y = -JUMP_STRENGTH
        JUMPING = True

# Atualiza o pulo do jogador
def update_jump():
    global VELOCITY_Y, JUMPING, img_rect, GRAVITY
    if JUMPING:
        VELOCITY_Y += GRAVITY
        img_rect.y += VELOCITY_Y
        if img_rect.bottom >= HEIGHT:
            img_rect.bottom = HEIGHT
            JUMPING = False
            VELOCITY_Y = 0

# Atualiza o pulo / queda do alvo chutado
def update_target_physics():
    global target_velocity_x, target_velocity_y, target_jumping, target_rect, target_gravity

    # Aplica gravidade no alvo chutado
    if target_jumping:
        target_velocity_y += target_gravity
        target_rect.x += target_velocity_x
        target_rect.y += target_velocity_y

        # Limita para o chão
        if target_rect.bottom >= HEIGHT:
            target_rect.bottom = HEIGHT
            target_jumping = False
            target_velocity_x = 0
            target_velocity_y = 0
        else:
            # Pode adicionar um pouco de atrito para a velocidade X ir diminuindo
            target_velocity_x *= 0.95

# Função para "chutar" o alvo
def kick():
    global target_velocity_x, target_velocity_y, target_jumping, target_rect, img_rect

    # Só chuta se estiver perto o suficiente
    dist_x = target_rect.centerx - img_rect.centerx
    dist_y = target_rect.centery - img_rect.centery
    distancia = (dist_x ** 2 + dist_y ** 2) ** 0.5

    if distancia < 150:  # alcance do chute
        target_velocity_x = 20 if dist_x > 0 else -20  # lança para a direita ou esquerda
        target_velocity_y = -20  # pulo forte para cima ao ser chutado
        target_jumping = True

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detectar redimensionamento
    current_width, current_height = screen.get_size()
    if current_width != last_width or current_height != last_height:
        WIDTH, HEIGHT = current_width, current_height
        centralize_image()
        if background_orig:
            background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
        last_width, last_height = current_width, current_height

    # Teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimentação do jogador
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED

    # Pulo
    if keys[pygame.K_SPACE]:
        jump()

    # Chute
    if keys[pygame.K_f]:  # tecla F para chutar
        kick()

    # Limitar movimento do jogador e alvo
    limit_movement(img_rect)
    limit_movement(target_rect)

    # Atualizar física do pulo
    update_jump()
    update_target_physics()

    # Desenhar fundo
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Desenhar personagem principal
    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)  # fallback

    # Desenhar personagem alvo
    if target_img:
        screen.blit(target_img, target_rect.topleft)
    else:
        pygame.draw.rect(screen, (0, 255, 0), target_rect)  # fallback

    # Atualizar display
    pygame.display.flip()

pygame.quit()
