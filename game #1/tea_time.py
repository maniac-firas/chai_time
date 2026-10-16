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

b_width = biscuit_img.get_width()
b_height = biscuit_img.get_height()
q_height = b_height // 4

quarter_imgs = []
for i in range(4):
    q_rect = pygame.Rect(0, i * q_height, b_width, q_height if i < 3 else b_height - 3 * q_height)
    quarter_imgs.append(biscuit_img.subsurface(q_rect).copy())

glass_rect = empty_glass_img.get_rect(centerx=300, bottom=800)
tea_rect = tea_img.get_rect(centerx=glass_rect.centerx, bottom=glass_rect.bottom)

full_tea_height = float(tea_img.get_height())
top_layer_orig_width = top_layer_img.get_width()
top_layer_orig_height = top_layer_img.get_height()

font = pygame.font.SysFont("Arial", 36, bold=True)
sub_font = pygame.font.SysFont("Arial", 24)

target_quarter_sample = quarter_imgs[0].copy()
target_overlay = pygame.Surface(target_quarter_sample.get_size(), pygame.SRCALPHA)
target_overlay.fill((60, 30, 5, 150))
target_quarter_sample.blit(target_overlay, (0, 0))

def spawn_new_biscuit():
    global active_quarters, active_soak_timers
    global dragging, grab_offset_x, grab_offset_y, vel_x, vel_y, biscuit_rect
    global spawn_cooldown, is_spawning_cooldown, has_been_grabbed

    active_quarters = list(range(4))
    active_soak_timers = [0.0] * 4

    dragging = False
    grab_offset_x = 0
    grab_offset_y = 0
    vel_x = 0
    vel_y = 0
    has_been_grabbed = False

    init_x = glass_rect.right + 20
    init_y = 550
    total_h = sum(quarter_imgs[i].get_height() for i in active_quarters)
    biscuit_rect = pygame.Rect(init_x, init_y, b_width, total_h)
    
    spawn_cooldown = 0.0
    is_spawning_cooldown = False

def reset_game():
    global is_broken, fallen_quarter_img, fallen_quarter_pos
    global tea_height, empty_wait_timer, is_refill_animating, game_over

    is_broken = False
    fallen_quarter_img = None
    fallen_quarter_pos = [0, 0]

    tea_height = full_tea_height
    empty_wait_timer = 0.0
    is_refill_animating = False
    game_over = False

    spawn_new_biscuit()

GRAVITY = 0.5
MASS = 1.0
SPRING_STIFFNESS = 0.15
DAMPING = 0.85

WIN_TIME = 1.8
FAIL_TIME = 2.0

clock = pygame.time.Clock()

reset_game()

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not is_spawning_cooldown:
            if event.button == 1:
                if biscuit_rect.collidepoint(event.pos):
                    dragging = True
                    has_been_grabbed = True
                    grab_offset_x = event.pos[0] - biscuit_rect.x
                    grab_offset_y = event.pos[1] - biscuit_rect.y

        elif event.type == pygame.MOUSEBUTTONUP and not game_over:
            if event.button == 1:
                dragging = False

    if game_over or is_spawning_cooldown:
        dragging = False

    if is_spawning_cooldown:
        spawn_cooldown += dt
        if spawn_cooldown >= 2.0:
            spawn_new_biscuit()

    current_tea_h = int(tea_height)
    in_tea = False
    if current_tea_h > 0:
        tea_collision_rect = pygame.Rect(
            tea_rect.x, 
            tea_rect.bottom - current_tea_h, 
            tea_rect.width, 
            current_tea_h
        )
        if biscuit_rect.colliderect(tea_collision_rect):
            in_tea = True

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
    elif has_been_grabbed and not game_over and not is_spawning_cooldown:
        if in_tea:
            vel_y += GRAVITY * 0.2
            vel_x *= 0.95
            vel_y *= 0.95
        else:
            vel_y += GRAVITY
            
        biscuit_rect.x += int(vel_x)
        biscuit_rect.y += int(vel_y)
    else:
        vel_x = 0
        vel_y = 0

    if biscuit_rect.left < 0:
        biscuit_rect.left = 0
        vel_x = 0
    if biscuit_rect.right > 600:
        biscuit_rect.right = 600
        vel_x = 0
    if biscuit_rect.top < 0:
        biscuit_rect.top = 0
        vel_y = 0

    if not dragging and has_been_grabbed and not game_over and not is_spawning_cooldown:
        if current_tea_h > 0 and tea_rect.x <= biscuit_rect.centerx <= tea_rect.right:
            tea_top = tea_rect.bottom - current_tea_h
            if biscuit_rect.top >= tea_top:
                is_broken = True
                game_over = True
                dragging = False
                broken_q_idx = active_quarters.pop() if active_quarters else 0

                fallen_quarter_img = quarter_imgs[broken_q_idx].copy()
                overlay = pygame.Surface(fallen_quarter_img.get_size(), pygame.SRCALPHA)
                overlay.fill((60, 30, 5, 160))
                fallen_quarter_img.blit(overlay, (0, 0))

                fallen_quarter_pos = [
                    tea_rect.centerx - fallen_quarter_img.get_width() // 2,
                    glass_rect.bottom - fallen_quarter_img.get_height() - 20
                ]

                if len(active_quarters) > 0:
                    new_h = sum(quarter_imgs[i].get_height() for i in active_quarters)
                    biscuit_rect.height = new_h
                else:
                    biscuit_rect.height = 0

    if biscuit_rect.bottom >= 800 and not game_over and not is_spawning_cooldown:
        biscuit_rect.bottom = 800
        game_over = True
        dragging = False

    glass_wall_margin = 15
    glass_inner_left = glass_rect.left + glass_wall_margin
    glass_inner_right = glass_rect.right - glass_wall_margin

    if biscuit_rect.bottom > glass_rect.top:
        if biscuit_rect.centerx < glass_rect.centerx and biscuit_rect.right > glass_inner_left and biscuit_rect.left < glass_inner_left:
            biscuit_rect.right = glass_inner_left
            vel_x = 0
        elif biscuit_rect.centerx > glass_rect.centerx and biscuit_rect.left < glass_inner_right and biscuit_rect.right > glass_inner_right:
            biscuit_rect.left = glass_inner_right
            vel_x = 0

    if current_tea_h > 0 and not is_refill_animating and len(active_quarters) > 0 and not game_over and not is_spawning_cooldown:
        active_q_idx = active_quarters[-1]

        q_y_offset = sum(quarter_imgs[i].get_height() for i in active_quarters[:-1])
        q_h = quarter_imgs[active_q_idx].get_height()
        q_world_rect = pygame.Rect(biscuit_rect.x, biscuit_rect.y + q_y_offset, biscuit_rect.width, q_h)

        if in_tea:
            if dragging:
                buoyancy = 0.8
                drag_resistance = 0.8

                vel_x *= drag_resistance
                vel_y *= drag_resistance
                vel_y -= buoyancy

            overlap_rect = biscuit_rect.clip(tea_collision_rect)
            
            horiz_overlap = min(biscuit_rect.right, tea_collision_rect.right) - max(biscuit_rect.left, tea_collision_rect.left)
            vert_overlap = min(biscuit_rect.bottom, tea_collision_rect.bottom) - max(biscuit_rect.top, tea_collision_rect.top)

            if vert_overlap < horiz_overlap or (biscuit_rect.left >= tea_collision_rect.left and biscuit_rect.right <= tea_collision_rect.right):
                base_decrease_speed = 0.1
                depth_factor = 0.00002
                overlap_area = overlap_rect.width * overlap_rect.height
                tea_height = max(0.0, tea_height - (base_decrease_speed + overlap_area * depth_factor))

        if q_world_rect.colliderect(tea_collision_rect):
            active_soak_timers[active_q_idx] += dt
            t = active_soak_timers[active_q_idx]

            if t >= FAIL_TIME and not is_broken:
                is_broken = True
                game_over = True
                broken_q_idx = active_quarters.pop()

                fallen_quarter_img = quarter_imgs[broken_q_idx].copy()
                overlay = pygame.Surface(fallen_quarter_img.get_size(), pygame.SRCALPHA)
                overlay.fill((60, 30, 5, 160))
                fallen_quarter_img.blit(overlay, (0, 0))

                fallen_quarter_pos = [
                    tea_rect.centerx - fallen_quarter_img.get_width() // 2,
                    glass_rect.bottom - fallen_quarter_img.get_height() - 20
                ]

                if len(active_quarters) > 0:
                    new_h = sum(quarter_imgs[i].get_height() for i in active_quarters)
                    biscuit_rect.height = new_h
        else:
            t = active_soak_timers[active_q_idx]
            if WIN_TIME <= t < FAIL_TIME and not is_broken:
                active_quarters.pop()
                if len(active_quarters) > 0:
                    new_h = sum(quarter_imgs[i].get_height() for i in active_quarters)
                    biscuit_rect.height = new_h
                else:
                    biscuit_rect.height = 0
                    is_spawning_cooldown = True
                    spawn_cooldown = 0.0

    if tea_height <= 0 and not is_refill_animating:
        empty_wait_timer += dt
        if empty_wait_timer >= 3.0:
            is_refill_animating = True
            empty_wait_timer = 0.0

    if is_refill_animating:
        tea_height += 1.5
        if tea_height >= full_tea_height:
            tea_height = full_tea_height
            is_refill_animating = False

    screen.blit(bg_img, (0, 0))

    target_x = 20
    target_y = 400 - (target_quarter_sample.get_height() // 2)
    screen.blit(target_quarter_sample, (target_x, target_y))
    pygame.draw.rect(screen, (255, 255, 255), (target_x, target_y, target_quarter_sample.get_width(), target_quarter_sample.get_height()), 2)

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

    if fallen_quarter_img:
        screen.blit(fallen_quarter_img, fallen_quarter_pos)

    screen.blit(empty_glass_img, glass_rect)

    if not is_spawning_cooldown and len(active_quarters) > 0:
        curr_y = biscuit_rect.y
        for q_idx in active_quarters:
            img = quarter_imgs[q_idx].copy()
            s_timer = active_soak_timers[q_idx]

            if s_timer > 0.5:
                darken_timer = s_timer - 0.5
                dark_ratio = min(1.0, darken_timer / 1.5)
                overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                overlay.fill((60, 30, 5, int(160 * dark_ratio)))
                img.blit(overlay, (0, 0))

            screen.blit(img, (biscuit_rect.x, curr_y))
            curr_y += img.get_height()

    if game_over:
        overlay_screen = pygame.Surface((600, 800), pygame.SRCALPHA)
        overlay_screen.fill((0, 0, 0, 180))
        screen.blit(overlay_screen, (0, 0))

        txt_go = font.render("GAME OVER", True, (255, 60, 60))
        txt_sub = sub_font.render("Press SPACE to Restart", True, (255, 255, 255))

        screen.blit(txt_go, txt_go.get_rect(center=(300, 380)))
        screen.blit(txt_sub, txt_sub.get_rect(center=(300, 430)))

    pygame.display.flip()

pygame.quit()
sys.exit()