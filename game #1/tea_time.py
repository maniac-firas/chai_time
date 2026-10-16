import pygame
import sys
import os

pygame.init()

screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("test_game")

assets_dir = os.path.join(os.path.dirname(__file__), "assets")

bg_img = pygame.image.load(os.path.join(assets_dir, "bg.png")).convert()
empty_glass_img = pygame.image.load(os.path.join(assets_dir, "Empty_Glass.png")).convert_alpha()
tea_img = pygame.image.load(os.path.join(assets_dir, "Tea.png")).convert_alpha()
top_layer_img = pygame.image.load(os.path.join(assets_dir, "top_layer.png")).convert_alpha()
biscuit_img = pygame.image.load(os.path.join(assets_dir, "Biscuit.png")).convert_alpha()

bg_img = pygame.transform.scale(bg_img, (600, 800))

empty_glass_img = pygame.transform.scale(
    empty_glass_img, 
    (int(empty_glass_img.get_width() * 0.75), int(empty_glass_img.get_height() * 0.75))
)
tea_img = pygame.transform.scale(
    tea_img, 
    (int(tea_img.get_width() * 0.75), int(tea_img.get_height() * 0.75))
)
top_layer_img = pygame.transform.scale(
    top_layer_img,
    (int(top_layer_img.get_width() * 0.75), int(top_layer_img.get_height() * 0.75))
)

biscuit_img = pygame.transform.scale(
    biscuit_img,
    (int(biscuit_img.get_width() * 0.60), int(biscuit_img.get_height() * 0.60))
)
biscuit_img = pygame.transform.rotate(biscuit_img, -90)

glass_rect = empty_glass_img.get_rect(centerx=300, bottom=800)
tea_rect = tea_img.get_rect(centerx=glass_rect.centerx, bottom=glass_rect.bottom)

biscuit_rect = biscuit_img.get_rect(topleft=(200, 200))

tea_height = float(tea_img.get_height())
full_tea_height = float(tea_img.get_height())
top_layer_orig_width = top_layer_img.get_width()
top_layer_orig_height = top_layer_img.get_height()

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
                if biscuit_rect.collidepoint(event.pos):
                    dragging = True
                    grab_offset_x = event.pos[0] - biscuit_rect.x
                    grab_offset_y = event.pos[1] - biscuit_rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        pivot_x = biscuit_rect.x + grab_offset_x
        pivot_y = biscuit_rect.y + grab_offset_y

        force_x = (mouse_pos[0] - pivot_x) * SPRING_STIFFNESS
        force_y = (mouse_pos[1] - pivot_y) * SPRING_STIFFNESS + (GRAVITY * MASS)

        vel_x = (vel_x + force_x / MASS) * DAMPING
        vel_y = (vel_y + force_y / MASS) * DAMPING

        biscuit_rect.x += int(vel_x)
        biscuit_rect.y += int(vel_y)
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
        if biscuit_rect.colliderect(tea_collision_rect):
            buoyancy = 0.8
            drag_resistance = 0.8
            
            vel_x *= drag_resistance
            vel_y *= drag_resistance
            vel_y -= buoyancy

            overlap_rect = biscuit_rect.clip(tea_collision_rect)
            overlap_area = overlap_rect.width * overlap_rect.height
            
            base_decrease_speed = 0.1
            depth_factor = 0.00002
            
            tea_height = max(0.0, tea_height - (base_decrease_speed + overlap_area * depth_factor))

    screen.blit(bg_img, (0, 0))

    current_tea_h = int(tea_height)
    if current_tea_h > 0:
        ratio = tea_height / full_tea_height
        
        width_reduction_factor = 0.35
        scaled_ratio = 1.0 - (1.0 - ratio) * width_reduction_factor

        crop_area = pygame.Rect(
            0, 
            int(full_tea_height - current_tea_h), 
            tea_rect.width, 
            current_tea_h
        )
        draw_pos = (tea_rect.x, tea_rect.bottom - current_tea_h)
        screen.blit(tea_img, draw_pos, crop_area)

        tea_decreased = full_tea_height - tea_height
        top_layer_y_offset = 0 if tea_decreased < 18 else -12

        scaled_width = max(1, int(top_layer_orig_width * scaled_ratio))
        scaled_top_layer = pygame.transform.scale(
            top_layer_img, 
            (scaled_width, top_layer_orig_height)
        )

        top_layer_draw_rect = scaled_top_layer.get_rect(
            centerx=tea_rect.centerx,
            top=(tea_rect.bottom - current_tea_h) + top_layer_y_offset
        )
        screen.blit(scaled_top_layer, top_layer_draw_rect)

    screen.blit(empty_glass_img, glass_rect)
    screen.blit(biscuit_img, biscuit_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()