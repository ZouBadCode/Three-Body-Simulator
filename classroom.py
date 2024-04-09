import math
class Physics:
    @staticmethod
    def calculate_gravitational_force(body1, body2):
        G = 10  # 簡化的G值
        dx = body2.pos[0] - body1.pos[0]
        dy = body2.pos[1] - body1.pos[1]
        distance_squared = dx**2 + dy**2

        # 軟化長度，防止除以零
        softening_length = 5
        distance_squared += softening_length**2

        distance = math.sqrt(distance_squared)
        force_magnitude = G * body1.mass * body2.mass / distance_squared
        force_direction = [dx / distance, dy / distance]

        return [force_magnitude * force_direction[0], force_magnitude * force_direction[1]]

    @staticmethod
    def update_velocity(body, forces):
        ax = sum([f[0] for f in forces]) / body.mass
        ay = sum([f[1] for f in forces]) / body.mass
        body.vel[0] += ax
        body.vel[1] += ay



import pygame
class Body:
    def __init__(self, pos, vel, mass, color):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.color = color
        self.trajectory = Trajectory(color)

    def update_position(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.trajectory.add_point(self.pos)


    def draw(self, screen, camera):
        adjusted_pos = camera.apply(self.pos)
        self.trajectory.draw(screen, camera)
        pygame.draw.circle(screen, self.color, adjusted_pos, 5)



class Trajectory:
    def __init__(self, color, max_length=50):
        self.points = []
        self.color = color
        self.max_length = max_length

    def add_point(self, pos):
        if len(self.points) > self.max_length:
            self.points.pop(0)
        self.points.append((int(pos[0]), int(pos[1])))

    def draw(self, screen, camera):
        if len(self.points) > 1:
            adjusted_points = [camera.apply(point) for point in self.points]
            pygame.draw.lines(screen, self.color, False, adjusted_points, 1)



class Camera:
    def __init__(self):
        self.offset = [0, 0]
        self.dragging = False
        self.target = None  # 追蹤目標
        self.drag_start = (0, 0)
        self.target = None  # 新增追蹤目標

    def set_target(self, new_target):
        self.target = new_target

    def start_drag(self, pos):
        self.dragging = True
        self.drag_start = pos

    def end_drag(self):
        self.dragging = False

    def update(self, pos):
        if self.dragging:
            dx = pos[0] - self.drag_start[0]
            dy = pos[1] - self.drag_start[1]
            self.offset[0] += dx
            self.offset[1] += dy
            self.drag_start = pos
        elif self.target:
            self.offset = [400 - self.target.pos[0], 300 - self.target.pos[1]]


    def apply(self, pos):
        return [pos[0] + self.offset[0], pos[1] + self.offset[1]]
    


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        

    def draw(self, screen, outline=None):
        # 如果需要畫外框
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (255, 255, 255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # 檢查鼠標位置
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
