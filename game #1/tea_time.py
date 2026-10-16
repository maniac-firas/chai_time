import pygame
import sys
import os

pygame.init()

screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("test_game")

assets_dir = os.path.join(os.path.dirname(__file__), "assets")

empty_glass_img = pygame.image.load(os.path.join(assets_dir, "Empty_Glass.png")).convert_alpha()
tea_img = pygame.image.load(os.path.join(assets_dir, "Tea.png")).convert_alpha()

empty_glass_img = pygame.transform.scale(
    empty_glass_img, 
    (int(empty_glass_img.get_width() * 0.75), int(empty_glass_img.get_height() * 0.75))
)
tea_img = pygame.transform.scale(
    tea_img, 
    (int(tea_img.get_width() * 0.75), int(tea_img.get_height() * 0.75))
)

glass_rect = empty_glass_img.get_rect(centerx=300, bottom=800)
tea_rect = tea_img.get_rect(centerx=glass_rect.centerx, bottom=glass_rect.bottom)

biscuit = pygame.Rect(200, 200, 100, 200)

tea_height = float(tea_img.get_height())
full_tea_height = tea_img.get_height()

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

    current_tea_h = int(tea_height)
    if current_tea_h > 0:
        tea_collision_rect = pygame.Rect(
            tea_rect.x, 
            tea_rect.bottom - current_tea_h, 
            tea_rect.width, 
            current_tea_h
        )
        if biscuit.colliderect(tea_collision_rect):
            buoyancy = 0.8
            drag_resistance = 0.8
            
            vel_x *= drag_resistance
            vel_y *= drag_resistance
            vel_y -= buoyancy

            tea_height = max(0.0, tea_height - 0.2)

    screen.fill((255, 255, 255))

    current_tea_h = int(tea_height)
    if current_tea_h > 0:
        crop_area = pygame.Rect(
            0, 
            full_tea_height - current_tea_h, 
            tea_rect.width, 
            current_tea_h
        )
        draw_pos = (tea_rect.x, tea_rect.bottom - current_tea_h-18)
        screen.blit(tea_img, draw_pos, crop_area)

    screen.blit(empty_glass_img, glass_rect)
    pygame.draw.rect(screen, (255, 0, 0), biscuit)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()