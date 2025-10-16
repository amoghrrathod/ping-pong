import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winner = None
        self.winning_score = 5

        pygame.mixer.init()
        try:
            self.paddle_sound = pygame.mixer.Sound("paddle_hit.wav")
            self.wall_sound = pygame.mixer.Sound("wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("score.wav")
        except pygame.error:
            self.paddle_sound = None
            self.wall_sound = None
            self.score_sound = None

    def reset_game(self, winning_score=5):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner = None
        self.winning_score = winning_score

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"

    def update(self):
        if not self.game_over:
            if self.ball.move() and self.wall_sound:
                self.wall_sound.play()
            
            if self.ball.check_collision(self.player, self.ai) and self.paddle_sound:
                self.paddle_sound.play()

            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
                if self.score_sound:
                    self.score_sound.play()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()
                if self.score_sound:
                    self.score_sound.play()

            self.ai.auto_track(self.ball, self.height)
            self.check_game_over()

    def render(self, screen):
        screen.fill((0, 0, 0))
        if self.game_over:
            win_font = pygame.font.SysFont("Arial", 50)
            win_text = f"{self.winner} Wins!"
            win_render = win_font.render(win_text, True, WHITE)
            win_rect = win_render.get_rect(center=(self.width / 2, self.height / 2 - 50))
            screen.blit(win_render, win_rect)

            replay_font = pygame.font.SysFont("Arial", 30)
            replay_text = "Play Again: Best of (3), (5), (7) or (ESC) to Exit"
            replay_render = replay_font.render(replay_text, True, WHITE)
            replay_rect = replay_render.get_rect(center=(self.width / 2, self.height / 2 + 20))
            screen.blit(replay_render, replay_rect)
        else:
            # Draw paddles and ball
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            # Draw score
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))
