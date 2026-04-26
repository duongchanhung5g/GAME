import pygame
import sys
import random
import os

pygame.init()

# ===== SCREEN =====
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LEVEL 11 - DODGE BOMB")

clock = pygame.time.Clock()

# ===== SOUND =====
try:
    pygame.mixer.init()
    sound_ok = True
except:
    sound_ok = False

# ===== LOAD =====
heart = pygame.image.load("heart.png")
heart = pygame.transform.scale(heart, (30,30))

jumpscare_img = None
if os.path.exists("download.jpg"):
    jumpscare_img = pygame.image.load("download.jpg")
    jumpscare_img = pygame.transform.scale(jumpscare_img, (WIDTH, HEIGHT))

scream_sound = None
if sound_ok and os.path.exists("scream.mp3"):
    scream_sound = pygame.mixer.Sound("scream.mp3")

# ===== COLORS =====
WHITE = (255,255,255)
BLACK = (0,0,0)
CYAN = (0,255,255)
RED = (255,0,0)

font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 60)

state = "tutorial"
played_scream = False

# ===== RESET =====
def reset_game():
    global heart_x, heart_y, lives
    global bombs, heals
    global mode, mode_timer, game_timer
    global end_phase, end_timer
    global played_scream

    heart_x = WIDTH//2
    heart_y = HEIGHT//2
    lives = 20

    bombs = []
    heals = []

    mode = "dodge"
    mode_timer = 0
    game_timer = 0

    end_phase = False
    end_timer = 0

    played_scream = False

    if sound_ok and os.path.exists("bonus.mp3"):
        pygame.mixer.music.load("bonus.mp3")
        pygame.mixer.music.play(-1)

# ===== TUTORIAL =====
def draw_tutorial():
    screen.fill((240,220,255))

    y = 80
    title = big_font.render("LEVEL 11 - NE BOMB", True, BLACK)
    screen.blit(title, title.get_rect(center=(WIDTH//2, y)))

    y += 100
    lines = [
        "W A S D: Di chuyen trai tim",
        "Ne bomb de song sot",
        "Song 4 phut 20 giay de chien thang",
        "Moi 30s: hoi mau 10s",
        "3 GIAY CUOI SE CUC KY HON LOAN 😈",
        "Nhan ENTER de bat dau"
    ]

    for line in lines:
        screen.blit(font.render(line, True, BLACK), (100, y))
        y += 40

# ===== INIT =====
reset_game()

# ===== LOOP =====
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == "tutorial" and event.key == pygame.K_RETURN:
                reset_game()
                state = "play"

            if event.key == pygame.K_r:
                reset_game()
                state = "tutorial"

    # ===== TUTORIAL =====
    if state == "tutorial":
        draw_tutorial()
        pygame.display.flip()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()

    # ===== GAME =====
    if state == "play":

        # MOVE
        if keys[pygame.K_a]: heart_x -= 5
        if keys[pygame.K_d]: heart_x += 5
        if keys[pygame.K_w]: heart_y -= 5
        if keys[pygame.K_s]: heart_y += 5

        heart_x = max(10, min(WIDTH-10, heart_x))
        heart_y = max(10, min(HEIGHT-10, heart_y))

        # TIMER
        game_timer += 1
        mode_timer += 1

        # MODE SWITCH
        if mode == "dodge" and mode_timer > 30*70:
            mode = "heal"
            mode_timer = 0
        elif mode == "heal" and mode_timer > 10*70:
            mode = "dodge"
            mode_timer = 0

        # SPAWN
        if not end_phase:
            if mode == "dodge":
                if random.random() < 0.25:
                    bombs.append([random.randint(0, WIDTH), -10, random.randint(6,10)])
            else:
                if random.random() < 0.12:
                    heals.append([random.randint(0, WIDTH), -10])

        # UPDATE BOMB
        hit = False
        for bomb in bombs[:]:
            bomb[1] += bomb[2]

            if abs(bomb[0]-heart_x) < 15 and abs(bomb[1]-heart_y) < 15:
                if not end_phase:  # bất tử ở cuối
                    lives -= 5
                bombs.remove(bomb)
                hit = True

            elif bomb[1] > HEIGHT:
                bombs.remove(bomb)

        # UPDATE HEAL
        for h in heals[:]:
            h[1] += 4

            if abs(h[0]-heart_x) < 15 and abs(h[1]-heart_y) < 15:
                lives += 1
                heals.remove(h)

            elif h[1] > HEIGHT:
                heals.remove(h)

        # LOSE
        if lives <= 0 and not end_phase:
            state = "lose"
            if sound_ok:
                pygame.mixer.music.stop()

        # ===== END PHASE =====
        if not end_phase and game_timer > 257*70:
            end_phase = True
            end_timer = 0
            lives = max(lives, 1)  # không chết ngu 😈

        if end_phase:
            end_timer += 1

            # spam bomb nhưng tránh player
            for _ in range(15):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)

                if abs(x - heart_x) < 60 and abs(y - heart_y) < 60:
                    continue

                bombs.append([x, y, random.randint(6,12)])

            if end_timer > 3*70:
                state = "win"

        # DRAW
        if lives <= 5:
            screen.fill((50,0,0))
        else:
            screen.fill(BLACK)

        # glitch
        for _ in range(3):
            y = random.randint(0, HEIGHT)
            pygame.draw.line(screen, (random.randint(100,255),0,0), (0,y), (WIDTH,y))

        # bomb
        for bomb in bombs:
            pygame.draw.circle(screen, WHITE, (int(bomb[0]), int(bomb[1])), 6)

        # heal
        for h in heals:
            pygame.draw.circle(screen, CYAN, (int(h[0]), int(h[1])), 6)

        # heart
        screen.blit(heart, (heart_x-15, heart_y-15))

        # rung màn
        if hit:
            screen.blit(screen, (random.randint(-5,5), random.randint(-5,5)))

        # UI
        screen.blit(font.render(f"Lives: {lives}",True,WHITE),(10,10))
        screen.blit(font.render(f"Time: {game_timer//70}",True,WHITE),(300,10))
        screen.blit(font.render(f"Mode: {mode}",True,WHITE),(600,10))

    # ===== LOSE =====
    if state == "lose":
        if jumpscare_img:
            screen.blit(jumpscare_img, (0,0))

        if sound_ok and scream_sound and not played_scream:
            scream_sound.play()
            played_scream = True

    # ===== WIN =====
    if state == "win":
        screen.fill((0,0,0))

        text = big_font.render("WIN", True, (180,0,0))
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

        for i in range(25):
            x = WIDTH//2 - 100 + i*8
            y = HEIGHT//2 + 50
            length = random.randint(20,60)
            pygame.draw.line(screen, (150,0,0), (x,y), (x,y+length), 3)

    pygame.display.flip()
    clock.tick(70)
