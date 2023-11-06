import pygame
import random
import math
import datetime 

pygame.init()

# 게임 화면 초기화
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("균형 감각 1 - 막대 수직 맞추기")
small_font = pygame.font.SysFont('malgungothic', 36)
# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
d_green = (243,118,7) # 지금은 주황색 코드임
green = (181,214,146)

# 게임 변수
stick_length = height*0.4
stick_thickness = 2
stick_angle = 90
stick_pivot = (width // 2, height // 2)
stick_tip_x_1 = stick_pivot[0] + stick_length * math.sin(math.radians(stick_angle))
stick_tip_x_2 = stick_pivot[0] - stick_length * math.sin(math.radians(stick_angle))
stick_tip_y_1 = stick_pivot[1] - stick_length * math.cos(math.radians(stick_angle))
stick_tip_y_2 = stick_pivot[1] + stick_length * math.cos(math.radians(stick_angle))

angle_speed = 1  # 회전 속도

clock = pygame.time.Clock()
angle = []
running = True
key_pressed_spacebar = False
font = pygame.font.Font(None, 50)

timer_text = font.render("4", True, d_green)
start_time = None  # 타이머 시작 시간을 추적하기 위한 변수
countdown = 4  # 카운트다운 시작값
count = 0
score = [0,0]
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(black)
    info_text = small_font.render("막대 수직 -> SpaceBar", True, white)
    screen.blit(info_text, (10, 10))
    pygame.draw.circle(screen, green, (width // 2, height // 2), 30)
    if not game_over:
        # 방향키 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            stick_angle += angle_speed
        if keys[pygame.K_RIGHT]:
            stick_angle -= angle_speed
        # 스페이스바 입력    
        if not key_pressed_spacebar:
            if keys[pygame.K_SPACE]:  # 예를 들어, 스페이스바를 입력으로 받아들임
                angle.append(min(stick_angle%180,180-stick_angle%180))
                count+=1
                key_pressed_spacebar = True  # 키 입력을 처리했음을 표시
                stick_angle = random.randint(0,360)
                countdown = 4

        if key_pressed_spacebar and not keys[pygame.K_SPACE]:  # 키가 놓여질 때 key_pressed를 재설정합니다.
            key_pressed_spacebar = False

        stick_tip_x_1 = stick_pivot[0] + stick_length * math.sin(math.radians(stick_angle))
        stick_tip_x_2 = stick_pivot[0] - stick_length * math.sin(math.radians(stick_angle))
        stick_tip_y_1 = stick_pivot[1] - stick_length * math.cos(math.radians(stick_angle))
        stick_tip_y_2 = stick_pivot[1] + stick_length * math.cos(math.radians(stick_angle))

        
        pygame.draw.line(screen, green, (stick_tip_x_1, stick_tip_y_1), (stick_tip_x_2, stick_tip_y_2), stick_thickness)

        # 중간하단에 위치

        current_time = pygame.time.get_ticks()

        if start_time is None:
            start_time = current_time
        elif current_time - start_time >= 1000:  # 1초 경과 시
            countdown -= 1
            if countdown > 0:
                timer_text = font.render(str(countdown), True, d_green)
            else:
                angle.append(1e9)
                count+=1
                timer_text = font.render("Time's up!", True, d_green)
                start_time = None
                countdown = 4

            start_time = current_time
            
        timer_rect = timer_text.get_rect()
        timer_rect.centerx = width // 2
        timer_rect.centery = height // 2 
        screen.blit(timer_text, timer_rect)
        pygame.display.update()
        clock.tick(60)

        if count == 15:
            for ang in angle:
                if ang > 5: # 채점 기준치 : 오차가 5도가 넘어가면 0점
                    score[0] += 10
                    score[1] += 1
                    continue
                score[0] += ang
        
            score[0] = round((150 - score[0])/15*10,2)
            game_over=True
            
    
        
    if game_over:
        screen.fill(black)
        print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+ "\t막대 수직 만들기\tScore: " + str(score[0]) +"\t0 points: "+str(score[1])+ "\n")
        with open("score.txt", "a") as file:
            file.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+ "\t막대 수직\tScore: " + str(score[0]) +"\t(0points): "+str(score[1])+ "\n")
        running = False
        
    
    pygame.display.update()
pygame.quit()
