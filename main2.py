import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1000, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Janela com Imagem")

BG_COLOR = (30, 30, 40)

image_file = "GAME\player.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

else:
    print("Imagem não encontrada!")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    screen.blit(img, img_rect.topleft)

    pygame.display.flip()



# Finalizar o Pygame

pygame.quit()

