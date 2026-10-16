import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("test_game")

rect = pygame.Rect(350, 350, 100, 100)

dragging = False
offset_x = 0
offset_y = 0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rect.collidepoint(event.pos):
                    dragging = True
                    offset_x = rect.x - event.pos[0]
                    offset_y = rect.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                rect.x = event.pos[0] + offset_x
                rect.y = event.pos[1] + offset_y

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()