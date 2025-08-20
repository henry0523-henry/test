import pygame
import sys

# 게임 설정
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = (40, 60)
PLATFORM_COLOR = (100, 100, 100)

# 색상
RED = (255, 80, 80)
BLUE = (80, 180, 255)
BG = (30, 30, 30)

# 플랫폼 정보
PLATFORMS = [
    pygame.Rect(100, 500, 600, 20),
    pygame.Rect(200, 400, 100, 20),
    pygame.Rect(500, 350, 100, 20),
    pygame.Rect(350, 250, 100, 20),
    pygame.Rect(700, 200, 60, 20),
]

# 플레이어 클래스
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, *PLAYER_SIZE)
        self.color = color
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.controls = controls

    def handle_input(self, keys):
        speed = 5
        if keys[self.controls['left']]:
            self.vel.x = -speed
        elif keys[self.controls['right']]:
            self.vel.x = speed
        else:
            self.vel.x = 0
        if keys[self.controls['jump']] and self.on_ground:
            self.vel.y = -13

    def update(self, platforms):
        gravity = 0.6
        self.vel.y += gravity
        self.rect.x += int(self.vel.x)
        self.collide(platforms, dx=True)
        self.rect.y += int(self.vel.y)
        self.on_ground = False
        self.collide(platforms, dx=False)

    def collide(self, platforms, dx):
        for plat in platforms:
            if self.rect.colliderect(plat):
                if dx:
                    if self.vel.x > 0:
                        self.rect.right = plat.left
                    elif self.vel.x < 0:
                        self.rect.left = plat.right
                    self.vel.x = 0
                else:
                    if self.vel.y > 0:
                        self.rect.bottom = plat.top
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = plat.bottom
                    self.vel.y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# 메인 함수
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2인 협동 플랫폼 게임')
    clock = pygame.time.Clock()

    # 플레이어1: 화살표키, 플레이어2: WASD
    p1 = Player(120, 440, RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP})
    p2 = Player(180, 440, BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w})

    goal1 = pygame.Rect(720, 160, 30, 40)
    goal2 = pygame.Rect(750, 160, 30, 40)

    font = pygame.font.SysFont(None, 36)
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if not win:
            p1.handle_input(keys)
            p2.handle_input(keys)
            p1.update(PLATFORMS)
            p2.update(PLATFORMS)
            if p1.rect.colliderect(goal1) and p2.rect.colliderect(goal2):
                win = True

        screen.fill(BG)
        for plat in PLATFORMS:
            pygame.draw.rect(screen, PLATFORM_COLOR, plat)
        pygame.draw.rect(screen, (255, 200, 0), goal1)
        pygame.draw.rect(screen, (0, 255, 200), goal2)
        p1.draw(screen)
        p2.draw(screen)
        if win:
            text = font.render('축하합니다! 두 명 모두 도착!', True, (255,255,255))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
