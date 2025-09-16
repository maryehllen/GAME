import pygame


pygame.init()


WIDTH, HEIGHT = 1000, 250

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Janela Simples")


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    pygame.display.flip()


pygame.quit()
