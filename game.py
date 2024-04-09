import pygame
import math

from classroom import *


bodies = []

def stop_game():
    global running
    running = False


def add_body_game(pos, vel, mass, color):
    global bodies
    new_body = Body(pos, vel, mass, color)
    bodies.append(new_body)

def nima():
    
    global bodies

    # 初始化pygame
    pygame.init()

    # 設置屏幕大小
    screen = pygame.display.set_mode((1400, 800))

    camera = Camera()

    def draw_body_list(screen, bodies):
        font = pygame.font.SysFont('comicsans', 20)
        y_offset = 10
        for i, body in enumerate(bodies):
            text = font.render(f'Body {i+1}', 1, (255, 255, 255))
            pygame.draw.rect(screen, body.color, (10, y_offset, 20, 20))
            screen.blit(text, (35, y_offset))
            y_offset += 30
            
    def check_body_click(pos, bodies):
        y_offset = 10
        for i, body in enumerate(bodies):
            if pos[0] >= 10 and pos[0] <= 30 and pos[1] >= y_offset and pos[1] <= y_offset + 20:
                return body
            y_offset += 30
        return None


    # 創建暫停按鈕
    pause_button = Button((200, 200, 200), 900, 10, 100, 50, 'Pause')

    close_button = Button((200, 200, 200), 500, 10, 100, 50, 'Close')


    global running
    # 模擬
    target_state = False
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左鍵按下
                    clicked_body = check_body_click(event.pos, bodies)
                    if clicked_body:
                        camera.set_target(clicked_body)
                        target_state = True
                    else:
                        camera.start_drag(event.pos)
                        target_state = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左鍵鬆開
                    camera.end_drag()
            elif event.type == pygame.MOUSEMOTION:
                if camera.dragging:
                    if paused:
                        camera.update(event.pos)
                        screen.fill((0, 0, 0))  # 清屏
                        for body in bodies:
                            body.draw(screen,camera)
                    else:
                        camera.update(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.is_over(event.pos):
                    stop_game()
                if pause_button.is_over(event.pos):
                    paused = not paused
        pause_button.draw(screen, (0,0,0))
        close_button.draw(screen, (0,0,0))
        draw_body_list(screen, bodies)
        if not paused:
            screen.fill((0, 0, 0))  # 清屏
            pause_button.draw(screen, (0,0,0))
            close_button.draw(screen, (0,0,0))
            draw_body_list(screen, bodies)
            # 計算引力並更新速度
            for i in range(len(bodies)):
                forces = []
                for j in range(len(bodies)):
                    if i != j:
                        force = Physics.calculate_gravitational_force(bodies[i], bodies[j])
                        forces.append(force)
                Physics.update_velocity(bodies[i], forces)

            # 更新位置並繪製星體
            for body in bodies:
                body.update_position()
                body.draw(screen,camera)
            if target_state == True:
                camera.update(clicked_body)
        pygame.display.flip()  # 更新屏幕顯示
        pygame.time.delay(10)

    pygame.quit()
