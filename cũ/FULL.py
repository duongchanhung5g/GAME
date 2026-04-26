import pygame
import sys
import random
import os
pygame.init()

# ===== SCREEN =====
WIDTH, HEIGHT = 1200,620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME VIP")

# ===== MIXER =====
try:
    pygame.mixer.init()
    sound_ok = True
except:
    sound_ok = False

# ===== MUSIC =====
if sound_ok and os.path.exists("nhacnen.mp3"):
    pygame.mixer.music.load("nhacnen.mp3")
    pygame.mixer.music.play(-1)

# ===== JUMPSCARE (THÊM) =====
jumpscare_img = None
scream_sound = None
played_scream = False

if os.path.exists("download.jpg"):
    jumpscare_img = pygame.image.load("download.jpg")
    jumpscare_img = pygame.transform.scale(jumpscare_img, (WIDTH, HEIGHT))

if sound_ok and os.path.exists("scream.mp3"):
    scream_sound = pygame.mixer.Sound("scream.mp3")

clock = pygame.time.Clock()

# ===== COLORS =====
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
PINK = (255,105,180)
PURPLE = (160,32,240)
SKY_BLUE = (135, 206, 235)

font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 50)

# ===== GAME =====
MAX_LEVEL = 10

def reset_game():
    global level, score, lives, state
    global paddle_w, paddle_x
    global balls, bricks, items
    global played_scream   # THÊM

    level = 1
    score = 0
    lives = 5
    state = "tutorial"

    played_scream = False  # THÊM

    paddle_w = 120
    paddle_x = WIDTH//2 - paddle_w//2

    balls = [[WIDTH//2, HEIGHT//2, 4, -4]]
    items = []
    create_bricks()

# ===== PADDLE =====
paddle_h = 10
paddle_y = HEIGHT - 40
paddle_speed = 6

# ===== BALL =====
radius = 8

# ===== BRICKS =====
def create_bricks():
    global bricks
    bricks = []

    rows = 4 + level
    cols = 7
    brick_w = 70
    brick_h = 20
    pad = 6

    total_w = cols*brick_w + (cols-1)*pad
    start_x = (WIDTH - total_w)//2
    start_y = 50

    for r in range(rows):
        for c in range(cols):
            x = start_x + c*(brick_w+pad)
            y = start_y + r*(brick_h+pad)

            rect = pygame.Rect(x,y,brick_w,brick_h)

            if random.random() < 0.2:
                bricks.append([rect, 2, "move", random.choice([-1,1])])
            else:
                bricks.append([rect, 1, "normal", 0])

# ===== ITEM =====
def spawn_item(x, y):
    if level in [1,2,3,5,6,8] and random.random() < 0.2:
        loai = "bomb"
    elif level in [4,7,9,10] and random.random() < 0.5:
        loai = "bomb"
    else:
        loai = random.choice(["to","ball","life"])
    items.append([x,y,loai])

# ===== BOMB =====
def bomb_explode(x,y):
    global bricks, score
    for brick in bricks[:]:
        rect = brick[0]
        dist = ((rect.centerx-x)**2 + (rect.centery-y)**2)**0.5
        if dist < 80:
            bricks.remove(brick)
            score += 20

# ===== TUTORIAL =====
def draw_tutorial():
    screen.fill((240,220,255))

    y = 50
    title = big_font.render("HUONG DAN CHOI", True, BLACK)
    screen.blit(title, title.get_rect(center=(WIDTH//2, y)))

    y += 80
    lines = [
        "← → : Di chuyen paddle",
        "SPACE: Tang toc paddle",
        "Pha gach de qua man",
        f"Tong level: {MAX_LEVEL}",
        "Nhan ENTER de bat dau"
    ]

    for line in lines:
        screen.blit(font.render(line, True, BLACK), (50, y))
        y += 35

    y += 20

    pygame.draw.circle(screen, BLUE, (100,y), 8)
    screen.blit(font.render("Tang do dai paddle", True, BLACK),(120,y-10))
    y+=30

    pygame.draw.circle(screen, RED, (100,y), 8)
    screen.blit(font.render("Them bong", True, BLACK),(120,y-10))
    y+=30

    pygame.draw.circle(screen, GREEN, (100,y), 8)
    screen.blit(font.render("Them mang", True, BLACK),(120,y-10))
    y+=30

    pygame.draw.circle(screen, BLACK, (100,y), 8)
    screen.blit(font.render("Bomb: tru mau + no gach", True, BLACK),(120,y-10))

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
                state = "play"

            if event.key == pygame.K_r:
                reset_game()
                if sound_ok:
                    pygame.mixer.music.play(-1)

    # ===== TUTORIAL =====
    if state == "tutorial":
        draw_tutorial()
        pygame.display.flip()
        clock.tick(60)
        continue

    # ===== GAME =====
    screen.fill(SKY_BLUE)

    if state == "play":
        keys = pygame.key.get_pressed()
        speed = paddle_speed*2 if keys[pygame.K_SPACE] else paddle_speed

        if keys[pygame.K_LEFT]:
            paddle_x -= speed
        if keys[pygame.K_RIGHT]:
            paddle_x += speed

        paddle_x = max(0, min(WIDTH - paddle_w, paddle_x))

        # BALL
        for ball in balls[:]:
            ball[0]+=ball[2]
            ball[1]+=ball[3]

            if ball[0]<=0 or ball[0]>=WIDTH:
                ball[2]*=-1
            if ball[1]<=0:
                ball[3]*=-1

            if paddle_x<=ball[0]<=paddle_x+paddle_w and paddle_y<=ball[1]<=paddle_y+paddle_h:
                ball[3] = -abs(ball[3])

            for brick in bricks[:]:
                rect,hp,loai,_=brick
                if rect.collidepoint(ball[0],ball[1]):
                    brick[1]-=1
                    ball[3]*=-1
                    if brick[1]<=0:
                        bricks.remove(brick)
                        score+=50
                        if random.random()<0.4:
                            spawn_item(rect.centerx,rect.centery)
                    break

            if ball[1]>HEIGHT:
                balls.remove(ball)

        if len(balls)==0:
            lives-=1
            if lives>0:
                balls.append([WIDTH//2,HEIGHT//2,4,-4])
            else:
                state="lose"

        # MOVE BRICK
        for brick in bricks:
            rect,hp,loai,huong=brick
            if loai=="move":
                rect.x+=huong*2
                if rect.left<=0 or rect.right>=WIDTH:
                    brick[3]*=-1

        # ITEM
        for item in items[:]:
            item[1]+=4

            if paddle_x<=item[0]<=paddle_x+paddle_w and paddle_y<=item[1]<=paddle_y+paddle_h:

                if item[2]=="to":
                    paddle_w=min(WIDTH//3, paddle_w+15)

                elif item[2]=="ball":
                    balls.append([item[0],item[1],random.choice([-5,5]),-5])

                elif item[2]=="life":
                    lives+=1

                elif item[2]=="bomb":
                    lives-=5
                    paddle_w=max(40,paddle_w-60)
                    bomb_explode(item[0],item[1])

                    if lives<=0:
                        state="lose"
                        if sound_ok:
                            pygame.mixer.music.stop()

                items.remove(item)

            elif item[1]>HEIGHT:
                items.remove(item)

        # NEXT LEVEL
        if len(bricks)==0:
            if level<MAX_LEVEL:
                level+=1
                balls=[[WIDTH//2,HEIGHT//2,4,-4]]
                create_bricks()
            else:
                state="win"

    # ===== DRAW =====
    for ball in balls:
        pygame.draw.circle(screen, RED, (int(ball[0]),int(ball[1])), radius)

    pygame.draw.rect(screen, BLUE, (paddle_x,paddle_y,paddle_w,paddle_h))

    for rect,_,loai,_ in bricks:
        pygame.draw.rect(screen, PURPLE if loai=="move" else PINK, rect)

    for item in items:
        color = BLACK if item[2]=="bomb" else GREEN if item[2]=="life" else BLUE if item[2]=="to" else RED
        pygame.draw.circle(screen, color, (int(item[0]),int(item[1])),6)

    screen.blit(font.render(f"Score: {score}",True,BLACK),(10,10))
    screen.blit(font.render(f"Lives: {lives}",True,BLACK),(650,10))
    screen.blit(font.render(f"Level: {level}",True,BLACK),(350,10))

    # ===== LOSE =====
    if state=="lose":

        # 🔥 HIỆN ẢNH
        if jumpscare_img:
            screen.blit(jumpscare_img, (0,0))

        text = big_font.render("CON GA - Bam R De Choi Lai", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

        # 🔥 ÂM THANH (1 lần)
        if sound_ok:
            pygame.mixer.music.stop()
            if scream_sound and not played_scream:
                scream_sound.play()
                played_scream = True

    if state=="win":
        text = big_font.render("YOU WIN", True, GREEN)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

    pygame.display.flip()
    clock.tick(70)