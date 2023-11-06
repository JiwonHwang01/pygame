import pygame
import sys
import random
import datetime
# 게임 초기화
pygame.init()

# 화면 설정
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")
font = pygame.font.Font(None, 50)

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)

# 미로 파일 불러오기
mazes = []
current_maze = []
with open("maze.txt", "r") as file:
    for line in file:
        if line.strip() == "=====":
            mazes.append(current_maze)
            current_maze = []
        else:
            row = list(line.strip())
            current_maze.append(row)
maze = random.choice(mazes)

# 미로 셀 크기
cell_width = width // len(maze[0])
cell_height = height // len(maze)

# 플레이어 시작 위치
player_x, player_y = 1, 1

# 게임 루프
count = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and maze[player_y - 1][player_x] != '*':
                player_y -= 1
            if event.key == pygame.K_DOWN and maze[player_y + 1][player_x] != '*':
                player_y += 1
            if event.key == pygame.K_LEFT and maze[player_y][player_x - 1] != '*':
                player_x -= 1
            if event.key == pygame.K_RIGHT and maze[player_y][player_x + 1] != '*':
                player_x += 1
            count+=1

    screen.fill(black)

    # 미로 그리기
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == '*':
                pygame.draw.rect(screen, white, (col * cell_width, row * cell_height, cell_width, cell_height))
            if maze[row][col] =="E":
                pygame.draw.rect(screen, (0, 0, 0), (col * cell_width, row * cell_height, cell_width, cell_height))
                pygame.draw.rect(screen, (0, 255, 0), (col * cell_width + cell_width*0.3, row * cell_height+ cell_height*0.3, cell_width*0.4, cell_height*0.4))

    # 플레이어 그리기
    pygame.draw.rect(screen, (255, 0, 0), (player_x * cell_width, player_y * cell_height, cell_width, cell_height))
    
    pygame.display.update()

    # 게임 종료 조건 (목표 지점 도착)
    if maze[player_y][player_x] == 'E':
        screen.fill(black)
        print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+ "\t미로 게임\tCount: " + str(count) + "\n")
        with open("score.txt", "a") as file:
            file.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')+ "\t미로 게임\tCount: " + str(count) + "\n")
        running = False

pygame.quit()
sys.exit()