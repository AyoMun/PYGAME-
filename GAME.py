import pygame
import os
import math

# -------------------
# Initialization
# -------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# -------------------
# Data & Assets
# -------------------
PLATFORM_DATA = [
    {"start": 2.715, "end": 3.099}, {"start": 3.348, "end": 3.731}, {"start": 3.966, "end": 4.713}, 
    {"start": 5.208, "end": 5.613}, {"start": 5.864, "end": 6.251}, {"start": 6.498, "end": 7.159}, 
    {"start": 7.774, "end": 8.141}, {"start": 8.388, "end": 8.733}, {"start": 9.000, "end": 9.678}, 
    {"start": 10.262, "end": 10.611}, {"start": 10.895, "end": 11.230}, {"start": 11.526, "end": 12.211}, 
    {"start": 12.815, "end": 13.147}, {"start": 13.414, "end": 13.764}, {"start": 14.061, "end": 14.758}, 
    {"start": 15.319, "end": 15.648}, {"start": 15.929, "end": 16.308}, {"start": 16.588, "end": 17.236}, 
    {"start": 17.863, "end": 18.163}, {"start": 18.497, "end": 18.847}, {"start": 19.098, "end": 19.764}
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

player_frames = []
for f in ["frame1.png", "frame2.png", "frame3.png", "jump.png"]:
    player_frames.append(pygame.image.load(os.path.join(ASSETS_DIR, f)).convert_alpha())

pygame.mixer.music.load(os.path.join(ASSETS_DIR, "wait for you.mp3"))

# -------------------
# Constants
# -------------------
SCROLL_SPEED = 12
PLAYER_X = 150
PLATFORM_Y = 450
JUMP_DURATION = 0.6  # Seconds the jump lasts
MAX_JUMP_HEIGHT = 180
FALL_SPEED = 15

# -------------------
# Variables
# -------------------
player_rect = pygame.Rect(PLAYER_X, PLATFORM_Y - 128, 128, 128)
game_started = False
player_state = "RUNNING" # Options: "RUNNING", "JUMPING", "FALLING"
jump_start_time = 0
music_time = 0

# -------------------
# Main Loop
# -------------------
running = True
while running:
    if game_started:
        music_time = (pygame.mixer.music.get_pos() / 1000.0)
    
    screen.fill((20, 20, 35))
    keys = pygame.key.get_pressed()
    is_holding_space = keys[pygame.K_SPACE]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # RELEASE SPACE TO JUMP
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if not game_started:
                game_started = True
                pygame.mixer.music.play()
                
            if player_state == "RUNNING":
                player_state = "JUMPING"
                jump_start_time = music_time

    # --- PLATFORM TRACKING ---
    currently_over_platform = False
    
    # Intro Platform
    intro_x = (0 * 60 * SCROLL_SPEED) - (music_time * 60 * SCROLL_SPEED) + PLAYER_X
    intro_rect = pygame.Rect(intro_x, PLATFORM_Y, 2.5 * 60 * SCROLL_SPEED, 40)
    if intro_rect.right > 0:
        pygame.draw.rect(screen, (50, 50, 70), intro_rect)
        if intro_rect.collidepoint(PLAYER_X + 64, PLATFORM_Y + 5):
            currently_over_platform = True

    # Beat Platforms
    for p in PLATFORM_DATA:
        x_pos = (p['start'] * 60 * SCROLL_SPEED) - (music_time * 60 * SCROLL_SPEED) + PLAYER_X
        width = (p['end'] - p['start']) * 60 * SCROLL_SPEED
        plat_rect = pygame.Rect(x_pos, PLATFORM_Y, width, 40)
        if -width < x_pos < WIDTH:
            pygame.draw.rect(screen, (100, 100, 255), plat_rect)
            if plat_rect.collidepoint(PLAYER_X + 64, PLATFORM_Y + 5):
                currently_over_platform = True

    # --- PHYSICS STATE MACHINE ---
    if game_started:
        if player_state == "RUNNING":
            player_rect.bottom = PLATFORM_Y
            # If the platform ends or we let go of space without jumping, we fall
            if not currently_over_platform:
                player_state = "FALLING"

        elif player_state == "JUMPING":
            t = (music_time - jump_start_time) / JUMP_DURATION
            if t <= 1.0:
                # Parabolic Arc
                arc = 4 * MAX_JUMP_HEIGHT * t * (1 - t)
                player_rect.bottom = PLATFORM_Y - arc
                
                # SNAP MID-AIR: If we press space while falling in the arc
                if t > 0.5 and is_holding_space and currently_over_platform:
                    player_state = "RUNNING"
            else:
                player_state = "FALLING"

        elif player_state == "FALLING":
            player_rect.y += FALL_SPEED
            # CATCH: If we press space while passing a platform
            if is_holding_space and currently_over_platform:
                if player_rect.bottom >= PLATFORM_Y - 20: # Buffer to prevent teleporting from way above
                    player_state = "RUNNING"

    # --- RESET ---
    if player_rect.top > HEIGHT:
        pygame.mixer.music.stop()
        game_started = False
        player_rect.bottom = PLATFORM_Y
        player_state = "RUNNING"
        music_time = 0

    # --- DRAW ---
    frame = (int(pygame.time.get_ticks() / 100) % 3) if player_state == "RUNNING" else 3
    screen.blit(player_frames[frame], (player_rect.x, player_rect.y))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()