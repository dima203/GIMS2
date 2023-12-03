from random import choice

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


WINDOW_SIZE = (1920, 1080)
FPS = 60
SCORE = 0
TIME = 0
GAME_TIME = 1 * 60 * 1000
WHACK_SHOW_TIME = 1000
CURRENT_WHACK_SHOW_TIME = WHACK_SHOW_TIME


class WhackHole:
    x: int
    y: int
    size: int
    color: tuple[float, float, float]
    active_color: tuple[float, float, float]
    is_active: bool

    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int] = (255, 255, 255),
                 active_color: tuple[int, int, int] = (255, 100, 100)) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.color = color[0] / 255, color[1] / 255, color[2] / 255
        self.active_color = active_color[0] / 255, active_color[1] / 255, active_color[2] / 255
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def draw(self, window: pygame.Surface) -> None:
        window_center_x, window_center_y = window.get_width() // 2, window.get_height() // 2
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        p1 = (self.x - window_center_x) / window_center_x
        p2 = (self.y - window_center_y) / window_center_y
        p3 = (self.x + self.size - window_center_x) / window_center_x
        p4 = (self.y + self.size - window_center_y) / window_center_y
        glVertex2f(p1, p2)
        glVertex2f(p3, p2)
        glVertex2f(p3, p4)
        glVertex2f(p1, p4)

        if self.is_active:
            whack_size = self.size * 0.75
            offset = (self.size - whack_size) / 2
            p1 = (self.x + offset - window_center_x) / window_center_x
            p2 = (self.y + offset - window_center_y) / window_center_y
            p3 = (self.x + offset + whack_size - window_center_x) / window_center_x
            p4 = (self.y + offset + whack_size - window_center_y) / window_center_y
            glColor3f(*self.active_color)
            glVertex2f(p1, p2)
            glVertex2f(p3, p2)
            glVertex2f(p3, p4)
            glVertex2f(p1, p4)
        glEnd()
        glFlush()

    def check_click(self, mouse_x: int, mouse_y: int) -> bool:
        return self.x < mouse_x < self.x + self.size and self.y < mouse_y < self.y + self.size


def game_end() -> None:
    s = TIME // 1000
    m, s = divmod(TIME // 1000, 60)
    h, m = divmod(m, 60)
    print(SCORE, '\t', f'{h:02}:{m:02}:{s:02}')
    pygame.quit()
    quit()


def main():
    global SCORE
    global TIME
    global CURRENT_WHACK_SHOW_TIME

    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)

    clock = pygame.time.Clock()
    whack_time = 0

    glClearColor(0, 0, 0, 1)

    holes: list[WhackHole] = []
    holes.append(WhackHole(50, 50, 300))
    holes.append(WhackHole(400, 50, 300))
    holes.append(WhackHole(750, 50, 300))
    holes.append(WhackHole(1100, 50, 300))
    holes.append(WhackHole(1450, 50, 300))
    holes.append(WhackHole(50, 400, 300))
    holes.append(WhackHole(400, 400, 300))
    holes.append(WhackHole(750, 400, 300))
    holes.append(WhackHole(1100, 400, 300))
    holes.append(WhackHole(1450, 400, 300))
    holes.append(WhackHole(50, 750, 300))
    holes.append(WhackHole(400, 750, 300))
    holes.append(WhackHole(750, 750, 300))
    holes.append(WhackHole(1100, 750, 300))
    holes.append(WhackHole(1450, 750, 300))

    choice(holes).activate()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for hole in holes:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if hole.check_click(mouse_x, WINDOW_SIZE[1] - mouse_y):
                            if hole.is_active:
                                whack_time = 0
                                hole.deactivate()
                                SCORE += int(100 * (WHACK_SHOW_TIME / CURRENT_WHACK_SHOW_TIME))
                                choice(holes).activate()
                                break
                    else:
                        SCORE -= 50

        if TIME >= GAME_TIME:
            game_end()

        if whack_time > CURRENT_WHACK_SHOW_TIME:
            whack_time = 0
            for hole in holes:
                if hole.is_active:
                    hole.deactivate()
                    SCORE -= 100
                    choice(holes).activate()
                    break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for hole in holes:
            hole.draw(window)
        pygame.display.flip()
        clock.tick(FPS)
        TIME += clock.get_time()
        whack_time += clock.get_time()
        CURRENT_WHACK_SHOW_TIME = int(WHACK_SHOW_TIME / (TIME / 1000 / 60 * 2 + 1))
        print(CURRENT_WHACK_SHOW_TIME)


if __name__ == '__main__':
    main()
