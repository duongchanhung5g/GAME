import pygame
import sys
import random
import os
import math
pygame.init()
def run_dark_mode():
    # ===== SCREEN =====
    WIDTH, HEIGHT = 1000,600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GAME VIP")

    # ===== MIXER =====
    try:
        pygame.mixer.init()
        sound_ok = True
    except:
        sound_ok = False

    # ===== MUSIC =====
    if sound_ok and os.path.exists("bonus.mp3"):
        pygame.mixer.music.load("bonus.mp3")
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
        global played_scream
        global paused  # ===== PAUSE =====
        level = 1
        score = 0
        lives = 5
        state = "tutorial"

        played_scream = False
        paused = False  # ===== PAUSE =====

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
        nonlocal bricks
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
        # ===== TỈ LỆ BOMB THEO LEVEL =====
        if level in [1,2,3,5,6,8]:
            bomb_rate = 0.2   # 20%
        elif level in [4,7,9]:
            bomb_rate = 0.4   # 40%
        elif level == 10:
            bomb_rate = 0.6   # 60%
        else:
            bomb_rate = 0

        # ===== XÁC ĐỊNH ITEM =====
        if random.random() < bomb_rate:
            loai = "bomb"
        else:
            loai = random.choice(["to","ball","life"])

        items.append([x,y,loai])

    # ===== BOMB =====
    def bomb_explode(x,y):
        nonlocal bricks, score
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
            "Nhan ENTER de bat dau",
            "Nhan Esc de tam dung"
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

        pygame.draw.circle(screen, WHITE, (100,y), 8)
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

                # ===== PAUSE =====
                if event.key == pygame.K_ESCAPE:
                    paused = True

                if event.key == pygame.K_c:
                    paused = False

        # ===== PAUSE SCREEN =====
        if paused:
            screen.fill(SKY_BLUE)
            text = big_font.render("PAUSED - Bam C de choi tiep", True, BLACK)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            pygame.display.flip()
            clock.tick(60)
            continue

        # ===== TUTORIAL =====
        if state == "tutorial":
            draw_tutorial()
            pygame.display.flip()
            clock.tick(60)
            continue

        # ===== GAME =====
        screen.fill(BLACK)

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
                            if random.random()<0.7:
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
            color = WHITE if item[2]=="bomb" else GREEN if item[2]=="life" else BLUE if item[2]=="to" else RED
            pygame.draw.circle(screen, color, (int(item[0]),int(item[1])),6)

        screen.blit(font.render(f"Score: {score}",True,WHITE),(10,10))
        screen.blit(font.render(f"Lives: {lives}",True,WHITE),(650,10))
        screen.blit(font.render(f"Level: {level}",True,WHITE),(350,10))

        # ===== LOSE =====
        if state=="lose":

            if jumpscare_img:
                screen.blit(jumpscare_img, (0,0))

            text = big_font.render("CON GA - Bam R De Choi Lai", True, RED)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

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
def run_day_mode():
    # ===== SCREEN =====
    WIDTH, HEIGHT = 1000,600
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
        global played_scream
        global paused  # ===== PAUSE =====

        level = 1
        score = 0
        lives = 5
        state = "tutorial"

        played_scream = False
        paused = False  # ===== PAUSE =====

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
        # ===== TỈ LỆ BOMB THEO LEVEL =====
        if level in [1,2,3,5,6,8]:
            bomb_rate = 0.2   # 20%
        elif level in [4,7,9]:
            bomb_rate = 0.4   # 40%
        elif level == 10:
            bomb_rate = 0.6   # 60%
        else:
            bomb_rate = 0

        # ===== XÁC ĐỊNH ITEM =====
        if random.random() < bomb_rate:
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
            "Nhan ENTER de bat dau",
            "Nhan Esc de tam dung"
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

                # ===== PAUSE =====
                if event.key == pygame.K_ESCAPE:
                    paused = True

                if event.key == pygame.K_c:
                    paused = False

        # ===== PAUSE SCREEN =====
        if paused:
            screen.fill(SKY_BLUE)
            text = big_font.render("PAUSED - Bam C de choi tiep", True, BLACK)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
            pygame.display.flip()
            clock.tick(60)
            continue

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
                            if random.random()<0.7:
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

            if jumpscare_img:
                screen.blit(jumpscare_img, (0,0))

            text = big_font.render("CON GA - Bam R De Choi Lai", True, RED)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

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
def lvl_11():
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

    # ===== THÊM =====
    glitch_img = None
    if os.path.exists("glitch.jpg"):
        glitch_img = pygame.image.load("glitch.jpg")
        glitch_img = pygame.transform.scale(glitch_img, (WIDTH, HEIGHT))

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
    YELLOW = (255,255,0)

    font = pygame.font.SysFont("arial", 22)
    big_font = pygame.font.SysFont("arial", 60)

    state = "tutorial"
    paused = False
    played_scream = False

    # ===== RESET =====
    def reset_game():
        global heart_x, heart_y, lives
        global bombs, heals, blasters
        global mode, mode_timer, game_timer
        global end_phase, end_timer
        global played_scream, paused

        # ===== THÊM =====
        global final_30s, glitch_timer, blast_delay, spawned_wave
        global red_flash_timer

        heart_x = WIDTH//2
        heart_y = HEIGHT//2
        lives = 20

        bombs = []
        heals = []
        blasters = []

        mode = "dodge"
        mode_timer = 0
        game_timer = 0

        end_phase = False
        end_timer = 0

        # ===== THÊM =====
        final_30s = False
        glitch_timer = 0
        blast_delay = 0
        spawned_wave = False

        # ===== EFFECT =====
        red_flash_timer = 0

        played_scream = False
        paused = False

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
            "Ne bomb + laser de song sot",
            "Song 4 phut 20 giay de chien thang",
            "Moi 30s: hoi mau 10s",
            "ESC: Pause | C: Continue",
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

                if event.key == pygame.K_ESCAPE and state == "play":
                    paused = True

                if event.key == pygame.K_c:
                    paused = False

        # ===== PAUSE =====
        if paused and state == "play":
            screen.fill((20,20,20))
            text = big_font.render("PAUSED", True, WHITE)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
            sub = font.render("Nhan C de tiep tuc", True, WHITE)
            screen.blit(sub, sub.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
            pygame.display.flip()
            clock.tick(60)
            continue

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

            # ===== RED EFFECT TIMER =====
            if lives <= 5:
                red_flash_timer += 1
            else:
                red_flash_timer = 0

            # ===== FINAL 30s =====
            if not final_30s and game_timer > (230 * 70):
                final_30s = True
                glitch_timer = 0
                blast_delay = 0
                spawned_wave = False

                heart_x = WIDTH // 2
                heart_y = HEIGHT // 2

            if final_30s:
                glitch_timer += 1

                if glitch_timer < 70:
                    if not spawned_wave:
                        for _ in range(60):
                            x = random.randint(0, WIDTH)
                            y = random.randint(0, HEIGHT)

                            dx = (WIDTH//2) - x
                            dy = (HEIGHT//2) - y
                            dist = max(1, math.hypot(dx, dy))

                            dx /= dist
                            dy /= dist

                            blasters.append({
                                "x": x,
                                "y": y,
                                "dx": dx,
                                "dy": dy,
                                "timer": 0
                            })
                        spawned_wave = True

                elif glitch_timer > 70 + 105:
                    for b in blasters:
                        if b["timer"] < 30:
                            b["timer"] = 30

            # MODE SWITCH
            if mode == "dodge" and mode_timer > 30*70:
                mode = "heal"
                mode_timer = 0
            elif mode == "heal" and mode_timer > 10*70:
                mode = "dodge"
                mode_timer = 0

            # ===== SPAWN =====
            if not end_phase:
                if mode == "dodge":
                    # ===== BOMB SPAWN RATE =====
                    bomb_rate = 0.25

                    if final_30s:
                        bomb_rate = 0.4   # tăng nhẹ (bạn có thể chỉnh 0.3 → 0.4)

                    if random.random() < bomb_rate:
                        bombs.append([random.randint(0, WIDTH), -10, random.randint(6,10)])

                    if random.random() < 0.02:
                        x = random.randint(0, WIDTH)
                        y = -50

                        dx = heart_x - x
                        dy = heart_y - y
                        dist = max(1, math.hypot(dx, dy))

                        dx /= dist
                        dy /= dist

                        blasters.append({
                            "x": x,
                            "y": y,
                            "dx": dx,
                            "dy": dy,
                            "timer": 0
                        })
                else:
                    if random.random() < 0.12:
                        heals.append([random.randint(0, WIDTH), -10])

            # ===== UPDATE =====
            hit = False
            for bomb in bombs[:]:
                bomb[1] += bomb[2]

                if abs(bomb[0]-heart_x) < 15 and abs(bomb[1]-heart_y) < 15:
                    if not end_phase:
                        lives -= 1
                    bombs.remove(bomb)
                    hit = True

                elif bomb[1] > HEIGHT:
                    bombs.remove(bomb)

            for h in heals[:]:
                h[1] += 4

                if abs(h[0]-heart_x) < 15 and abs(h[1]-heart_y) < 15:
                    lives += 1
                    heals.remove(h)

                elif h[1] > HEIGHT:
                    heals.remove(h)

            for b in blasters[:]:
                b["timer"] += 1

                if b["timer"] < 30:
                    continue

                if b["timer"] < 60:
                    px = heart_x - b["x"]
                    py = heart_y - b["y"]
                    proj = px*b["dx"] + py*b["dy"]

                    if proj > 0:
                        cx = b["x"] + b["dx"] * proj
                        cy = b["y"] + b["dy"] * proj

                        if math.hypot(heart_x - cx, heart_y - cy) < 12:
                            if not end_phase:
                                lives -= 0.1
                else:
                    blasters.remove(b)

            # LOSE
            if lives <= 0.9 and not end_phase:
                state = "lose"
                if sound_ok:
                    pygame.mixer.music.stop()

            # ===== END PHASE =====
            if not end_phase and game_timer > 257*70:
                end_phase = True
                end_timer = 0
                lives = max(lives, 1)

            if end_phase:
                end_timer += 1

                for _ in range(15):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)

                    if abs(x - heart_x) < 60 and abs(y - heart_y) < 60:
                        continue

                    bombs.append([x, y, random.randint(6,12)])

                if end_timer > 3*70:
                    state = "win"

            # ===== DRAW =====
            if lives <= 5:
                red_intensity = random.randint(40,130)
                screen.fill((red_intensity,0,0))

                for _ in range(5):
                    y = random.randint(0, HEIGHT)
                    pygame.draw.line(screen,(random.randint(150,255),0,0),(0,y),(WIDTH,y),2)
            else:
                screen.fill(BLACK)

            # glitch
            if final_30s and glitch_timer < 70 and glitch_img:
                screen.blit(glitch_img, (0,0))
            for _ in range(3):
                y = random.randint(0, HEIGHT)
                pygame.draw.line(screen, (random.randint(100,255),0,0), (0,y), (WIDTH,y))

            # bomb
            for bomb in bombs:
                pygame.draw.circle(screen, WHITE, (int(bomb[0]), int(bomb[1])), 6)

            # heal
            for h in heals:
                pygame.draw.circle(screen, CYAN, (int(h[0]), int(h[1])), 6)

            # blaster
            for b in blasters:
                end_x = b["x"] + b["dx"] * 1200
                end_y = b["y"] + b["dy"] * 1200

                if b["timer"] < 30:
                    pygame.draw.line(screen, YELLOW, (b["x"], b["y"]), (end_x, end_y), 2)
                elif b["timer"] < 60:
                    pygame.draw.line(screen, CYAN, (b["x"], b["y"]), (end_x, end_y), 6)

                pygame.draw.circle(screen, WHITE, (int(b["x"]), int(b["y"])), 10)

            # heart
            screen.blit(heart, (heart_x-15, heart_y-15))

            # SCREEN SHAKE
            if lives <= 5:
                screen.blit(screen, (random.randint(-6,6), random.randint(-6,6)))

            if hit:
                screen.blit(screen, (random.randint(-5,5), random.randint(-5,5)))

            screen.blit(font.render(f"Lives: {int(lives)}",True,WHITE),(10,10))
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
def menu():
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MENU")

    font = pygame.font.SysFont("arial", 40)
    small_font = pygame.font.SysFont("arial", 25)

    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))

        # ===== TITLE =====
        title = font.render("GAME VIP MENU", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(WIDTH//2, 150)))

        # ===== OPTIONS =====
        opt1 = small_font.render("ENTER: Day Mode", True, (200,200,200))
        opt2 = small_font.render("SHIFT: Dark Mode", True, (200,200,200))
        opt3 = small_font.render("1: Level 11 (Dodge Bomb)", True, (200,200,200))

        screen.blit(opt1, (WIDTH//2 - 150, 300))
        screen.blit(opt2, (WIDTH//2 - 150, 350))
        screen.blit(opt3, (WIDTH//2 - 150, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ENTER → DAY
                if event.key == pygame.K_RETURN:
                    run_day_mode()

                # SHIFT → DARK
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    run_dark_mode()

                # PHÍM 1 → LEVEL 11
                if event.key == pygame.K_1:
                    lvl_11()

        clock.tick(60)
menu()