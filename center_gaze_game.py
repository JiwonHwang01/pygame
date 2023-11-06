import pygame
import sys
import random, math, itertools, datetime

# Pygame 초기화
pygame.init()

# 화면 설정
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shape Guessing Game")
small_font = pygame.font.SysFont('malgungothic', 36)

# 색깔 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (243,118,7)
green = (181,214,146)

# 게임 변수
score = [0,0]
font = pygame.font.Font(None, 36)

# 모양 리스트
shapes = ["circle", "rectangle", "triangle", "star"]

# 방향
dirction = ["up", "down", "left", "right"]
dir_cycle = itertools.cycle(dirction)
font2 = pygame.font.Font(None, 50)

# 현재 모양, 방향
current_shape = None
current_direction = None

# 모양 변경 시간과 스페이스바 누른 시간
next_shape_time = 0
next_direction_time = 0
spacebar_pressed_time = None

clock = pygame.time.Clock()
count = 0
game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    if not game_over:
        # 1초마다 모양 변경
        if current_time > next_shape_time:
            next_shape_time = current_time + 1000  # 1초마다
            current_shape = random.choice(shapes)
            spacebar_pressed_time = None  # 스페이스바를 누르지 않은 상태로 초기화
            
        if current_time > next_direction_time:
            next_direction_time = current_time + 5000  # 5초마다
            current_direction = next(dir_cycle)
            count += 1
        screen.fill(black)

        if count > 12:
            game_over = True
            
        # 현재 모양 그리기
        shape_size = 50
        if current_shape == "circle":
            pygame.draw.circle(screen, green, (width // 2, height // 2), shape_size // 2)
        elif current_shape == "rectangle":
            pygame.draw.rect(screen, green, (width // 2 - shape_size // 2, height // 2 - shape_size // 2, shape_size, shape_size))
        elif current_shape == "triangle":
            pygame.draw.polygon(screen, green, [(width // 2, height // 2 - shape_size // 2),
                                            (width // 2 - shape_size // 2, height // 2 + shape_size // 2),
                                            (width // 2 + shape_size // 2, height // 2 + shape_size // 2)])
        elif current_shape == "star":
            star_points = []
            star_size = 25
            for i in range(5):
                outer_angle = i * (2 * math.pi) / 5
                inner_angle = outer_angle + (math.pi / 5)
                outer_x = width // 2 + star_size * math.cos(outer_angle)
                outer_y = height // 2 + star_size * math.sin(outer_angle)
                inner_x = width // 2 + (star_size / 2) * math.cos(inner_angle)
                inner_y = height // 2 + (star_size / 2) * math.sin(inner_angle)
                star_points.extend([(outer_x, outer_y), (inner_x, inner_y)])
            pygame.draw.polygon(screen, green, star_points)

        
        if current_direction == "up":
            text = font2.render("UP", True, red)
            text_rect = text.get_rect()
            text_rect.center = (width // 2, 50)
        elif current_direction == "down":
            text = font2.render("DOWN", True, red)
            text_rect = text.get_rect()
            text_rect.center = (width // 2, height - 50)
        elif current_direction == "left":
            text = font2.render("LEFT", True, red)
            text_rect = text.get_rect()
            text_rect.center = (50, height // 2)
        elif current_direction == "right":
            text = font2.render("RIGHT", True, red)
            text_rect = text.get_rect()
            text_rect.center = (width - 60, height // 2)
        else:
            text = font.render("", True, red)
        
        screen.blit(text, text_rect)
        
        # 스페이스바 누르면 점수 증가
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and spacebar_pressed_time is None:
            if current_shape == "circle":
                score[0] += 1
            else:
                score[1] += 1
            spacebar_pressed_time = current_time

        # 점수 표시
        score_text = font.render("Score: " + str(score[0]-score[1]), True, white)
        screen.blit(score_text, (10, 10))
        info_text = font.render("Circle -> SpaceBar", True, white)
        screen.blit(info_text, (10, 50))
        
        
    if game_over:
        screen.fill(black)
        score_text = small_font.render("점수 : "+str(score[0]-score[1])+"점", True, white)
        score_rect = score_text.get_rect(center=(width // 2, height // 2))
        screen.blit(score_text, score_rect)
        
        # Enter 누르면 창 닫기
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            with open("score.txt", "a") as file:
                file.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+ "\t고개 & 시선\tScore: " + str(score[0]) +"\tMiss: " + str(score[1]) + "\n")
            running = False
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()