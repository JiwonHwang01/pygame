import pygame
import sys
import random
import time
import datetime

# 게임 초기화
pygame.init()
# 화면 설정
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("도형 좌우 맞히기(순간판단력, 동체시력)")
small_font = pygame.font.SysFont('malgungothic', 36)

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
green = (181,214,146)

# 화면 중앙에 수평으로 흰선 그리기
line_thickness = 2  # 선의 두께
line_y = width // 2  # 선의 위치 (중앙)

# 게임 변수
score = 0
font = pygame.font.Font(None, 36)
shapes = ["circle", "rect", "polygon"]
last_shape = None
next_shape_time = 0

clock = pygame.time.Clock()

# 방향키 누름 여부 변수
left_pressed = False
right_pressed = False
game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_pressed = True
            if event.key == pygame.K_RIGHT:
                right_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
            if event.key == pygame.K_RIGHT:
                right_pressed = False
            last_shape = random.choice(shapes)
            next_shape_time = current_time + 1.0 
            
            shape_x = random.randint(0, width - 50)  # 50은 도형 크기
            if width//2 - 50 <= shape_x <width//2:
                continue

    current_time = time.time()
    if not game_over:
        # 랜덤한 도형 생성
        if current_time > next_shape_time:
            next_shape_time = current_time + 1.0 
            last_shape = random.choice(shapes)
            
            # 도형의 위치를 랜덤하게 설정
            shape_x = random.randint(0, width - 50)  # 50은 도형 크기
            if width//2 - 50 <= shape_x <width//2:
                continue
       
        screen.fill(black)
        
        # 도형 그리기
        shape_size = 50
        if last_shape == "rect":
            pygame.draw.rect(screen, green, (shape_x, height // 2 - shape_size // 2, shape_size, shape_size))
        elif last_shape == "circle":
            pygame.draw.circle(screen, green, (shape_x + shape_size // 2, height // 2), shape_size // 2)
        else:
            pygame.draw.polygon(screen, green, ([shape_x + shape_size//2, height // 2],[shape_x, height // 2 + shape_size],[shape_x + shape_size, height // 2 + shape_size]))
        # 점수 표시
        score_text = font.render("Score: " + str(score), True, white)
        screen.blit(score_text, (10, 10))
        
        # 중앙 흰 선 그리기
        pygame.draw.line(screen, green, (line_y, 0), (line_y, height), line_thickness)

        # 게임 로직: 키 입력 처리
        if not left_pressed and not right_pressed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if shape_x < width//2 - 50:
                    score += 1
                else:
                    game_over = True
                left_pressed = True
            elif keys[pygame.K_RIGHT]:
                if shape_x > width//2:
                    score += 1
                else:
                    game_over = True 
                right_pressed = True
        if left_pressed and not keys[pygame.K_LEFT]:
            left_pressed = False
        if right_pressed and not keys[pygame.K_RIGHT]:
            right_pressed = False
            
    if game_over:
        screen.fill(black)
        score_text = small_font.render("점수 : "+str(score)+"점", True, white)
        score_rect = score_text.get_rect(center=(width // 2, height // 2))
    
        screen.blit(score_text, score_rect)
         
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            with open("score.txt", "a") as file:
                file.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+ "\t좌우 도형 보기\tScore: " + str(score) + "\n")
        
            running = False
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()