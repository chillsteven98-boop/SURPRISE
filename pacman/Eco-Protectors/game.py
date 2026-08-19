import pygame
import random
import sys
import os

# 1. Setup Game Window
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eco-Defender")
clock = pygame.time.Clock()
font = pygame.font.SysFont(["helvetica", "arial", "sans-serif"], 24, bold=True)

# 2. Physics & Gameplay Constants
GROUND_Y = HEIGHT - 100
GRAVITY = 0.25

# Actor Positions
flower_x = 100
flower_y = GROUND_Y - 100

human_x = WIDTH - 150
human_y = GROUND_Y - 90

# Lists to track active objects
trash_list = []       # Active flying trash: [x, y, x_vel, y_vel]
landed_trash = []     # Dirty stationary trash on ground: [x, y]
seed_list = []        # Active seeds: [x, y]

# Game Scoring & States
trash_dropped = 0
trash_cleared = 0
WIN_TARGET = 15
game_state = "PLAYING" # PLAYING, WIN, GAME_OVER
spawn_timer = 0

# 3. Load & Scale Sprite Assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(filename):
    return os.path.join(BASE_DIR, "assets", filename)

bg_img = pygame.transform.smoothscale(pygame.image.load(get_asset_path("background.png")).convert(), (WIDTH, HEIGHT))
sunflower_img = pygame.transform.smoothscale(pygame.image.load(get_asset_path("sunflower.png")).convert_alpha(), (80, 100))
litterer_img = pygame.transform.smoothscale(pygame.image.load(get_asset_path("litterer.png")).convert_alpha(), (75, 110))
seed_img = pygame.transform.smoothscale(pygame.image.load(get_asset_path("seed.png")).convert_alpha(), (20, 20))
trash_img = pygame.transform.smoothscale(pygame.image.load(get_asset_path("trash.png")).convert_alpha(), (30, 30))
bin_img = pygame.transform.smoothscale(pygame.image.load(get_asset_path("recycling_bin.png")).convert_alpha(), (50, 80))

# Pre-rotate landed trash for realistic tilted debris
landed_trash_img = pygame.transform.rotate(trash_img, 75)
landed_trash_img = pygame.transform.smoothscale(landed_trash_img, (30, 20))

def reset_game():
    """Resets all variables to start a fresh game."""
    global trash_dropped, trash_cleared, game_state, spawn_timer, trash_list, landed_trash, seed_list
    trash_dropped = 0
    trash_cleared = 0
    spawn_timer = 0
    game_state = "PLAYING"
    trash_list.clear()
    landed_trash.clear()
    seed_list.clear()

# 4. Main Loop
running = True
while running:
    # Draw Background (Sky & Grass are pre-rendered in image)
    screen.blit(bg_img, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # --- SHOOT SEEDS (While Playing) ---
            if game_state == "PLAYING" and event.key == pygame.K_SPACE:
                seed_list.append([flower_x + 30, flower_y + 20])
            
            # --- RESTART BUTTON SYSTEM ---
            if game_state in ["WIN", "GAME_OVER"] and event.key == pygame.K_r:
                reset_game()

    if game_state == "PLAYING":
        # --- TRASH GENERATION (Parabolic Launch) ---
        spawn_timer += 1
        if spawn_timer > 60: 
            x_velocity = -6.5 
            y_velocity = random.uniform(-9.5, -12.0) 
            trash_list.append([human_x, human_y, x_velocity, y_velocity])
            spawn_timer = 0

        # --- UPDATE SEEDS ---
        for seed in seed_list[:]:
            seed[0] += 10 
            if seed[0] > WIDTH:
                seed_list.remove(seed)

        # --- UPDATE TRASH WITH GRAVITY ---
        for trash in trash_list[:]:
            trash[0] += trash[2] 
            trash[1] += trash[3] 
            trash[3] += GRAVITY  

            # Condition A: Trash hits the floor
            if trash[1] >= GROUND_Y - 15:
                landed_trash.append([trash[0], GROUND_Y - 15])
                trash_list.remove(trash)
                trash_dropped += 1
                if trash_dropped >= 10:
                    game_state = "GAME_OVER"
                continue

            # Condition B: Seed hits active trash
            trash_rect = pygame.Rect(trash[0], trash[1], 30, 30)
            for seed in seed_list[:]:
                seed_rect = pygame.Rect(seed[0], seed[1], 20, 20)
                
                if trash_rect.colliderect(seed_rect):
                    if trash in trash_list:
                        trash_list.remove(trash)
                    if seed in seed_list:
                        seed_list.remove(seed)
                    trash_cleared += 1
                    if trash_cleared >= WIN_TARGET:
                        game_state = "WIN"
                    break 

        # --- DRAW ACTIVE ACTORS ---
        screen.blit(litterer_img, (human_x - 15, human_y - 15))
        screen.blit(sunflower_img, (flower_x, flower_y))

        # Draw Seeds
        for seed in seed_list:
            screen.blit(seed_img, (seed[0] - 10, seed[1] - 10))

        # Draw Flying Trash
        for trash in trash_list:
            screen.blit(trash_img, (trash[0], trash[1]))

        # Draw Landed Trash
        for litter in landed_trash:
            screen.blit(landed_trash_img, (litter[0], litter[1]))

        # Adding background color in render() enables pixel-perfect subpixel antialiasing!
        text_litter = font.render(f"Litter on Floor: {trash_dropped}/10", True, (200, 0, 0), (240, 240, 240))
        text_cleared = font.render(f"Trash Vaporized: {trash_cleared}/{WIN_TARGET}", True, (0, 100, 0), (240, 240, 240))
        
        # Calculate dynamic width to prevent any text bleeding on different screen resolutions
        box_width = max(text_litter.get_width(), text_cleared.get_width()) + 40
        
        # Draw Scoreboard HUD Box
        pygame.draw.rect(screen, (240, 240, 240), (10, 10, box_width, 90), border_radius=8)
        pygame.draw.rect(screen, (0, 100, 0), (10, 10, box_width, 90), width=2, border_radius=8)
        
        screen.blit(text_litter, (30, 20))
        screen.blit(text_cleared, (30, 56))

    elif game_state == "GAME_OVER":
        screen.fill((40, 40, 40))
        # Adding background color to render() enables pixel-perfect subpixel antialiasing!
        msg1 = font.render("BAD ENDING: Flora Destroyed.", True, (255, 100, 100), (40, 40, 40))
        msg2 = font.render("Human: 'I don't feel good...'", True, (255, 255, 255), (40, 40, 40))
        msg3 = font.render("No plants = No oxygen. Everyone suffocates.", True, (200, 200, 200), (40, 40, 40))
        msg_restart = font.render("Press [ R ] to Restart Game", True, (255, 255, 0), (40, 40, 40))
        screen.blit(msg1, (250, 180))
        screen.blit(msg2, (250, 240))
        screen.blit(msg3, (250, 300))
        screen.blit(msg_restart, (250, 400))

    elif game_state == "WIN":
        screen.fill((180, 230, 180))
        screen.blit(bin_img, (human_x - 100, GROUND_Y - 80))
        
        # Adding background color to render() enables pixel-perfect subpixel antialiasing!
        msg1 = font.render("GOOD ENDING: Eco-Success!", True, (0, 120, 0), (180, 230, 180))
        msg2 = font.render("Human: 'I feel bad for throwing garbage here.'", True, (0, 0, 0), (180, 230, 180))
        msg3 = font.render("They installed a proper recycling bin instead.", True, (60, 60, 60), (180, 230, 180))
        msg_restart = font.render("Press [ R ] to Play Again", True, (0, 0, 255), (180, 230, 180))
        screen.blit(msg1, (220, 180))
        screen.blit(msg2, (220, 240))
        screen.blit(msg3, (220, 300))
        screen.blit(msg_restart, (220, 400))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()