import pygame
import sys
import random

WIDTH, HEIGHT = 600, 800
BALL_RADIUS = 20
BALL_COLOR = (255, 80, 80)
BG_COLOR = (30, 30, 30)
PLATFORM_COLOR = (100, 200, 255)
GOAL_COLOR = (80, 255, 80)
FPS = 60

PLATFORMS = [
    pygame.Rect(100, 700, 400, 20),
    pygame.Rect(50, 600, 200, 20),
    pygame.Rect(350, 500, 200, 20),
    pygame.Rect(100, 400, 400, 20),
    pygame.Rect(200, 300, 200, 20),
]
GOAL = pygame.Rect(250, 50, 100, 30)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        speed = 6
        if keys[pygame.K_LEFT]:
            self.vx = -speed
        elif keys[pygame.K_RIGHT]:
            self.vx = speed
        else:
            self.vx = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -15
        gravity = 0.7
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy
        self.on_ground = False
        # 벽 충돌
        if self.x - BALL_RADIUS < 0:
            self.x = BALL_RADIUS
            self.vx = -self.vx * 0.7
        if self.x + BALL_RADIUS > WIDTH:
            self.x = WIDTH - BALL_RADIUS
            self.vx = -self.vx * 0.7
        if self.y - BALL_RADIUS < 0:
            self.y = BALL_RADIUS
            self.vy = 0
        if self.y + BALL_RADIUS > HEIGHT:
            self.y = HEIGHT - BALL_RADIUS
            self.vy = 0
            self.on_ground = True
        # 플랫폼 충돌
        ball_rect = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
        for plat in platforms:
            if ball_rect.colliderect(plat):
                if self.vy > 0 and self.y < plat.top:
                    self.y = plat.top - BALL_RADIUS
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0 and self.y > plat.bottom:
                    self.y = plat.bottom + BALL_RADIUS
                    self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('바운스볼')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    ball = Ball(WIDTH//2, HEIGHT-100)
    win = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if not win:
            ball.update(PLATFORMS)
            # 골 도달 체크
            ball_rect = pygame.Rect(ball.x - BALL_RADIUS, ball.y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
            if ball_rect.colliderect(GOAL):
                win = True
        screen.fill(BG_COLOR)
        for plat in PLATFORMS:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)
        pygame.draw.rect(screen, GOAL_COLOR, GOAL)
        ball.draw(screen)
        if win:
            text = font.render('클리어!', True, (255,255,0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 200))
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
