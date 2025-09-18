import pygame
import os
import time

pygame.init()

WIDTH, HEIGHT = 720, 420
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mover Imagem com Setas")

BG_COLOR = (193, 40, 40)

PLAYER_WIDTH, PLAYER_HEIGHT = 225, 225
TARGET_WIDTH, TARGET_HEIGHT = 225, 225

image_file = "player.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    img_rect = img.get_rect(midbottom=(WIDTH // 2, HEIGHT))
else:
    print("Imagem do personagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)

target_file = "patrick.png"
target_injured_file = "target_injured.png"
if os.path.exists(target_file):
    target_img = pygame.image.load(target_file).convert_alpha()
    target_img = pygame.transform.scale(target_img, (TARGET_WIDTH, TARGET_HEIGHT))
    target_rect = target_img.get_rect(midbottom=(WIDTH // 2 + 200, HEIGHT))
else:
    print("Imagem do personagem alvo não encontrada!")
    target_img = None
    target_rect = pygame.Rect(WIDTH // 2 + 200, HEIGHT - 50, TARGET_WIDTH, TARGET_HEIGHT)

background_file = "background.png"
if os.path.exists(background_file):
    background_orig = pygame.image.load(background_file).convert()
    background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
else:
    background_orig = None
    background = None
    print("Imagem de fundo não encontrada!")

SPEED = 3
JUMP_STRENGTH = 18
GRAVITY = 0.5
JUMPING = False
VELOCITY_Y = 0

target_velocity_x = 0
target_velocity_y = 0
target_jumping = False
target_gravity = GRAVITY

last_width, last_height = WIDTH, HEIGHT

target_damaged = False
damage_time = 0

def limit_movement(rect):
    if rect.left < 0:
        rect.left = 0
    if rect.right > WIDTH:
        rect.right = WIDTH
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > HEIGHT:
        rect.bottom = HEIGHT

def jump():
    global VELOCITY_Y, JUMPING
    if not JUMPING:
        VELOCITY_Y = -JUMP_STRENGTH
        JUMPING = True

def update_jump():
    global VELOCITY_Y, JUMPING, img_rect, GRAVITY
    if JUMPING:
        VELOCITY_Y += GRAVITY
        img_rect.y += VELOCITY_Y
        if img_rect.bottom >= HEIGHT:
            img_rect.bottom = HEIGHT
            JUMPING = False
            VELOCITY_Y = 0

def update_target_physics():
    global target_velocity_x, target_velocity_y, target_jumping, target_rect, target_gravity
    if target_jumping:
        target_velocity_y += target_gravity
        target_rect.x += target_velocity_x
        target_rect.y += target_velocity_y
        if target_rect.bottom >= HEIGHT:
            target_rect.bottom = HEIGHT
            target_jumping = False
            target_velocity_x = 0
            target_velocity_y = 0
    else:
        target_velocity_x *= 0.95

def kick():
    global target_velocity_x, target_velocity_y, target_jumping, target_rect, img_rect, target_damaged, damage_time
    dist_x = target_rect.centerx - img_rect.centerx
    dist_y = target_rect.centery - img_rect.centery
    distancia = (dist_x ** 2 + dist_y ** 2) ** 0.5

    if distancia < 150:
        target_velocity_x = 20 if dist_x > 0 else -20
        target_velocity_y = -20
        target_jumping = True
        target_damaged = True
        damage_time = pygame.time.get_ticks()

def detect_collision():
    global target_img, target_damaged, damage_time
    if target_damaged:
        if pygame.time.get_ticks() - damage_time <= 1000:
            if os.path.exists(target_injured_file):
                target_img = pygame.image.load(target_injured_file).convert_alpha()
                target_img = pygame.transform.scale(target_img, (TARGET_WIDTH, TARGET_HEIGHT))
        else:
            if os.path.exists(target_file):
                target_img = pygame.image.load(target_file).convert_alpha()
                target_img = pygame.transform.scale(target_img, (TARGET_WIDTH, TARGET_HEIGHT))
            target_damaged = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_width, current_height = screen.get_size()
    if current_width != last_width or current_height != last_height:
        WIDTH, HEIGHT = current_width, current_height
        img_rect.bottom = HEIGHT
        target_rect.bottom = HEIGHT
        if background_orig:
            background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
        last_width, last_height = current_width, current_height

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED
    if keys[pygame.K_SPACE]:
        jump()
    if keys[pygame.K_f]:
        kick()

    limit_movement(img_rect)
    limit_movement(target_rect)

    update_jump()
    update_target_physics()

    detect_collision()

    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)

    if target_img:
        screen.blit(target_img, target_rect.topleft)
    else:
        pygame.draw.rect(screen, (0, 255, 0), target_rect)

    pygame.display.flip()

pygame.quit()
