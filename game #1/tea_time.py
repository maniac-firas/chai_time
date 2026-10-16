import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("test_game")

biscuit = pygame.Rect(200, 200, 100, 200)
glass = pygame.Rect(300 - 100, 500, 200, 250)

tea_height = float(glass.height * 0.75)
tea = pygame.Rect(glass.x, glass.bottom - int(tea_height), glass.width, int(tea_height))

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

    if biscuit.colliderect(tea) and tea_height > 0:
        buoyancy = 0.8
        drag_resistance = 0.8
        
        vel_x *= drag_resistance
        vel_y *= drag_resistance
        vel_y -= buoyancy

        tea_height = max(0.0, tea_height - 0.2)
        tea.height = int(tea_height)
        tea.y = glass.bottom - tea.height

    screen.fill((0, 0, 0))
    if tea.height > 0:
        pygame.draw.rect(screen, (255, 255, 0), tea)
    pygame.draw.rect(screen, (255, 255, 255), biscuit)
    pygame.draw.rect(screen, (255, 255, 255), glass, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()