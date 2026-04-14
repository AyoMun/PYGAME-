import pygame
import time
import json

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCROLL_SPEED = 5 # Pixels per frame (adjust to match your game's pace)
PLATFORM_Y = 250 # The vertical position of the platforms
PLATFORM_HEIGHT = 20
BG_COLOR = (240, 240, 240)
PLATFORM_COLOR = (0, 0, 0)

# --- INITIALIZATION ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game Platform Generator")
clock = pygame.time.Clock()

# --- LOAD MUSIC ---
# Replace 'your_song.mp3' with your actual file path
pygame.mixer.music.load('assets/wait for you.mp3') 
pygame.mixer.music.play()

# --- DATA STORAGE ---
platforms = [] # Stores dicts: {'start_time': t1, 'end_time': t2}
current_platform_start = None
is_pressing = False

start_ticks = pygame.time.get_ticks()

running = True
while running:
    current_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Start creating platform on 'B' key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b and not is_pressing:
                is_pressing = True
                current_platform_start = current_time
        
        # Finish creating platform on 'B' key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_b and is_pressing:
                is_pressing = False
                platforms.append({
                    'start': current_platform_start,
                    'end': current_time
                })
                print(f"Platform created: {current_platform_start:.2f}s to {current_time:.2f}s")

    # --- DRAWING ---
    screen.fill(BG_COLOR)
    
    # Draw existing platforms
    for p in platforms:
        # Calculate horizontal position based on time and scroll speed
        # The 'offset' moves them left as time passes
        x_start = (p['start'] * 60 * SCROLL_SPEED) - (current_time * 60 * SCROLL_SPEED) + 100
        width = (p['end'] - p['start']) * 60 * SCROLL_SPEED
        
        # Only draw if on screen
        if x_start + width > 0:
            pygame.draw.rect(screen, PLATFORM_COLOR, (x_start, PLATFORM_Y, width, PLATFORM_HEIGHT))

    # Draw current platform being held
    if is_pressing:
        x_start = (current_platform_start * 60 * SCROLL_SPEED) - (current_time * 60 * SCROLL_SPEED) + 100
        width = (current_time - current_platform_start) * 60 * SCROLL_SPEED
        pygame.draw.rect(screen, (100, 100, 100), (x_start, PLATFORM_Y, width, PLATFORM_HEIGHT))

    # Static Character/Spawn Point Reference
    pygame.draw.rect(screen, (255, 0, 0), (100, PLATFORM_Y - 30, 20, 30)) # Red block represents player position

    pygame.display.flip()
    clock.tick(60)

# --- SAVE DATA ---
with open('level_data.json', 'w') as f:
    json.dump(platforms, f)
print("Level data saved to level_data.json")

pygame.quit()