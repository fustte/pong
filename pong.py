from random import randint
import pygame

# Configuración de pantalla
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
MARGIN = 30

# Colores (RGB: red, green, blue)
BG_COLOR = (0, 0, 0)
OBJ_COLOR = (200, 200, 200)

# Velocidades
PLAYER_SPEED = 10
BALL_SPEED = 10

# Configuración de pantalla y fuente
FPS = 60
SCORE_FONT_SIZE = 150
MESSAGE_FONT_SIZE = 25

class Drawable(pygame.Rect):
    def draw(self, screen):
        pygame.draw.rect(screen, OBJ_COLOR, self)

class Ball(Drawable):
    size = 10

    def __init__(self):
        super().__init__(
            (SCREEN_WIDTH - self.size) / 2,
            (SCREEN_HEIGHT - self.size) / 2,
            self.size,
            self.size)

        self.vel_y = randint(-BALL_SPEED, BALL_SPEED)
        self.vel_x = 0
        while self.vel_x == 0:
            self.vel_x = randint(-BALL_SPEED, BALL_SPEED)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y <= 0 or self.y >= (SCREEN_HEIGHT - self.size):
            self.vel_y = -self.vel_y

        if self.x <= 0:
            self.reset(True)
            return 2
        if self.x >= (SCREEN_WIDTH - self.size):
            self.reset(False)
            return 1
        return 0

    def reset(self, to_left):
        self.x = (SCREEN_WIDTH - self.size) / 2
        self.y = (SCREEN_HEIGHT - self.size) / 2
        self.vel_y = randint(-BALL_SPEED, BALL_SPEED)
        if to_left:
            self.vel_x = randint(-BALL_SPEED, -1)
        else:
            self.vel_x = randint(1, BALL_SPEED)

class Player(Drawable):
    def __init__(self, x):
        top = (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2
        super().__init__(x, top, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move_up(self):
        min_pos = 0
        self.y -= PLAYER_SPEED
        if self.y < min_pos:
            self.y = min_pos

    def move_down(self):
        max_pos = SCREEN_HEIGHT - PADDLE_HEIGHT
        self.y += PLAYER_SPEED
        if self.y > max_pos:
            self.y = max_pos

class Scoreboard:
    def __init__(self):
        self.init_font()
        self.reset()

    def init_font(self):
        available_fonts = pygame.font.get_fonts()
        font_name = 'ubuntu'
        if font_name not in available_fonts:
            font_name = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(font_name, SCORE_FONT_SIZE, True)

    def reset(self):
        self.scores = [0, 0]

    def draw(self, screen):
        n = 1
        for score in self.scores:
            score_text = str(score)
            score_img = self.font.render(score_text, True, OBJ_COLOR)
            img_width = score_img.get_width()
            x = n / 4 * SCREEN_WIDTH - img_width / 2
            y = MARGIN
            screen.blit(score_img, (x, y))
            n += 2

    def increment(self, player):
        if player in (1, 2):
            self.scores[player - 1] += 1

    def winner(self):
        if self.scores[0] == 9:
            return 1
        if self.scores[1] == 9:
            return 2
        return 0

class PongGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.init_font()

        self.ball = Ball()
        self.player1 = Player(MARGIN)
        self.player2 = Player(SCREEN_WIDTH - MARGIN - PADDLE_WIDTH)
        self.scoreboard = Scoreboard()

    def play(self):
        running = False
        winner = 0

        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    running = True
                if winner > 0 and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        running = True
                    elif event.key == pygame.K_s:
                        self.scoreboard.reset()
                        self.ball.reset(winner == 2)
                        winner = 0

            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_a]:
                self.player1.move_up()
            if key_state[pygame.K_z]:
                self.player1.move_down()
            if key_state[pygame.K_UP]:
                self.player2.move_up()
            if key_state[pygame.K_DOWN]:
                self.player2.move_down()

            self.screen.fill(BG_COLOR)

            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.draw_net()

            point_for = self.ball.move()
            self.ball.draw(self.screen)

            if self.ball.colliderect(self.player1) or self.ball.colliderect(self.player2):
                self.ball.vel_x = -self.ball.vel_x

            if point_for in (1, 2):
                self.scoreboard.increment(point_for)
                winner = self.scoreboard.winner()

            if winner > 0:
                self.ball.vel_x = self.ball.vel_y = 0
                self.announce_winner(winner)

            self.scoreboard.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def draw_net(self):
        net_x = SCREEN_WIDTH / 2
        painted_section = 20
        empty_section = 15
        net_width = 6

        for y in range(0, SCREEN_HEIGHT, painted_section + empty_section):
            pygame.draw.line(
                self.screen,
                OBJ_COLOR,
                (net_x, y),
                (net_x, y + painted_section),
                width=net_width)

    def init_font(self):
        available_fonts = pygame.font.get_fonts()
        font_name = 'ubuntu'
        if font_name not in available_fonts:
            font_name = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(font_name, MESSAGE_FONT_SIZE, True)

    def announce_winner(self, winner):
        messages = [
            f'Player {winner} wins!',
            f'Start a new game? (S/N)',
        ]
        y = SCREEN_HEIGHT / 2 - MESSAGE_FONT_SIZE
        for msg in messages:
            img_msg = self.font.render(msg, True, OBJ_COLOR, BG_COLOR)
            width = img_msg.get_width()
            x = (SCREEN_WIDTH - width) / 2
            self.screen.blit(img_msg, (x, y))
            y += MESSAGE_FONT_SIZE * 2

if __name__ == '__main__':
    PongGame().play()  