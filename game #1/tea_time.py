import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("test_game")

biscuit = pygame.Rect(200, 200, 100, 100)
glass = pygame.Rect(400 - 100, 500, 200, 250)

dragging = False
grab_offset_x = 0
grab_offset_y = 0

vel_x = 0
vel_y = 0

GRAVITY = 0.5
MASS = 1.0
SPRING_STIFFNESS = 0.15
DAMPING = 0.85

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if biscuit.collidepoint(event.pos):
                    dragging = True
                    grab_offset_x = event.pos[0] - biscuit.x
                    grab_offset_y = event.pos[1] - biscuit.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        pivot_x = biscuit.x + grab_offset_x
        pivot_y = biscuit.y + grab_offset_y

        force_x = (mouse_pos[0] - pivot_x) * SPRING_STIFFNESS
        force_y = (mouse_pos[1] - pivot_y) * SPRING_STIFFNESS + (GRAVITY * MASS)

        vel_x = (vel_x + force_x / MASS) * DAMPING
        vel_y = (vel_y + force_y / MASS) * DAMPING

        biscuit.x += int(vel_x)
        biscuit.y += int(vel_y)
    else:
        vel_x = 0
        vel_y = 0

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), biscuit)
    pygame.draw.rect(screen, (255, 255, 255), glass, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()