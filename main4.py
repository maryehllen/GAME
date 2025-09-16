import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Imagem com Setas e Pular com Espaço")

BG_COLOR = (30, 30, 40)

image_file = "player.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
else:
    print("Imagem não encontrada!")

SPEED = 1
JUMP_STRENGTH = 15
GRAVITY = 0.8

is_jumping = False
y_velocity = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED

    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        y_velocity = -JUMP_STRENGTH

    if is_jumping:
        img_rect.y += y_velocity

        y_velocity += GRAVITY

        if img_rect.bottom >= HEIGHT:
            img_rect.bottom = HEIGHT
            is_jumping = False
            y_velocity = 0

    screen.fill(BG_COLOR)

    screen.blit(img, img_rect.topleft)

    pygame.display.flip()

pygame.quit()
