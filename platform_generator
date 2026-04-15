import pygame
import os
import json

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SCROLL_SPEED = 5
PLATFORM_HEIGHT = 20
BG_COLOR = (20, 20, 35)
PLATFORM_COLOR = (100, 100, 255)
ACTIVE_PLATFORM_COLOR = (180, 180, 255)

# Y positions for each key (lower number = higher on screen)
PLATFORM_HEIGHTS = {
    pygame.K_3: 80,   # Highest
    pygame.K_w: 170,  # High
    pygame.K_a: 260,  # Middle
    pygame.K_c: 340,  # Low
}

HEIGHT_LABELS = {
    pygame.K_3: "3 - Highest",
    pygame.K_w: "W - High",
    pygame.K_a: "A - Middle",
    pygame.K_c: "C - Low",
}

HEIGHT_COLORS = {
    pygame.K_3: (255, 120, 120),
    pygame.K_w: (120, 255, 160),
    pygame.K_a: (100, 160, 255),
    pygame.K_c: (255, 220, 80),
}

COUNTDOWN_SECONDS = 4

# --- INITIALIZATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.init()
try:
    pygame.mixer.init()
    music_available = True
except pygame.error:
    music_available = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game Platform Generator")
clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 120)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)

# --- LOAD MUSIC ---
if music_available:
    try:
        pygame.mixer.music.load(os.path.join(BASE_DIR, 'assets', 'wait for you.mp3'))
    except pygame.error:
        music_available = False

# --- STATE ---
platforms = []
active_keys = {}  # key -> start_time when key was pressed
music_started = False
music_start_ticks = None
countdown_start_ticks = pygame.time.get_ticks()

def get_music_time():
    if music_start_ticks is None:
        return 0.0
    return (pygame.time.get_ticks() - music_start_ticks) / 1000.0

# --- MAIN LOOP ---
running = True
while running:
    now_ticks = pygame.time.get_ticks()
    elapsed_since_countdown = (now_ticks - countdown_start_ticks) / 1000.0
    countdown_value = COUNTDOWN_SECONDS - elapsed_since_countdown
    music_time = get_music_time()

    # Start music when countdown finishes
    if not music_started and countdown_value <= 0:
        music_started = True
        music_start_ticks = pygame.time.get_ticks()
        music_time = 0.0
        if music_available:
            pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if music_started:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in PLATFORM_HEIGHTS and key not in active_keys:
                    active_keys[key] = music_time

            if event.type == pygame.KEYUP:
                key = event.key
                if key in active_keys:
                    start_t = active_keys.pop(key)
                    end_t = music_time
                    if end_t > start_t:
                        platforms.append({
                            'start': round(start_t, 3),
                            'end': round(end_t, 3),
                            'y': PLATFORM_HEIGHTS[key]
                        })
                        print(f"Platform [{HEIGHT_LABELS[key]}]: {start_t:.2f}s to {end_t:.2f}s")

    # --- DRAWING ---
    screen.fill(BG_COLOR)

    if not music_started:
        # Draw countdown
        count_display = max(1, int(countdown_value) + 1)
        count_surf = font_large.render(str(count_display), True, (255, 255, 255))
        screen.blit(count_surf, count_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        get_ready = font_medium.render("Get ready to generate platforms!", True, (180, 180, 255))
        screen.blit(get_ready, get_ready.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)))

        # Draw key legend
        instructions = [
            (pygame.K_3, "3"),
            (pygame.K_w, "W"),
            (pygame.K_a, "A"),
            (pygame.K_c, "C"),
        ]
        legend_y = SCREEN_HEIGHT - 120
        label_surf = font_small.render("Hold keys to create platforms:", True, (200, 200, 200))
        screen.blit(label_surf, (20, legend_y - 24))
        for i, (k, display) in enumerate(instructions):
            color = HEIGHT_COLORS[k]
            txt = font_small.render(f"  [{display}]  {HEIGHT_LABELS[k]}", True, color)
            screen.blit(txt, (20 + i * 185, legend_y))
    else:
        # Draw placed platforms
        for p in platforms:
            x_start = (p['start'] * 60 * SCROLL_SPEED) - (music_time * 60 * SCROLL_SPEED) + 100
            width = (p['end'] - p['start']) * 60 * SCROLL_SPEED
            if x_start + width > 0 and x_start < SCREEN_WIDTH:
                # Determine color from y position
                color = PLATFORM_COLOR
                for k, y in PLATFORM_HEIGHTS.items():
                    if y == p['y']:
                        color = HEIGHT_COLORS[k]
                        break
                pygame.draw.rect(screen, color, (x_start, p['y'], width, PLATFORM_HEIGHT))

        # Draw currently-held platforms
        for key, start_t in active_keys.items():
            x_start = (start_t * 60 * SCROLL_SPEED) - (music_time * 60 * SCROLL_SPEED) + 100
            width = (music_time - start_t) * 60 * SCROLL_SPEED
            y = PLATFORM_HEIGHTS[key]
            color = HEIGHT_COLORS[key]
            light = tuple(min(255, c + 60) for c in color)
            pygame.draw.rect(screen, light, (x_start, y, max(4, width), PLATFORM_HEIGHT))

        # Player marker
        pygame.draw.rect(screen, (255, 80, 80), (85, 230, 20, 30))

        # Height guide lines
        for key, y in PLATFORM_HEIGHTS.items():
            color = HEIGHT_COLORS[key]
            dim = tuple(c // 3 for c in color)
            pygame.draw.line(screen, dim, (0, y + PLATFORM_HEIGHT // 2), (SCREEN_WIDTH, y + PLATFORM_HEIGHT // 2), 1)
            label = font_small.render(HEIGHT_LABELS[key], True, color)
            screen.blit(label, (SCREEN_WIDTH - label.get_width() - 6, y - 16))

        # Time display
        time_surf = font_small.render(f"Time: {music_time:.2f}s", True, (200, 200, 200))
        screen.blit(time_surf, (10, 10))

        # Platform count
        count_surf = font_small.render(f"Platforms: {len(platforms)}", True, (200, 200, 200))
        screen.blit(count_surf, (10, 32))

        # Key hints at bottom
        hint_surf = font_small.render("Hold [3] [W] [A] [C] to place platforms  |  Close window to save", True, (140, 140, 160))
        screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 16)))

    pygame.display.flip()
    clock.tick(60)

# --- SAVE DATA ---
with open(os.path.join(BASE_DIR, 'level_data.json'), 'w') as f:
    json.dump(platforms, f, indent=4)
print(f"Level data saved to level_data.json ({len(platforms)} platforms)")

pygame.quit()
