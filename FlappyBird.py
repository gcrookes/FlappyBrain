from xml.dom.expatbuilder import FilterVisibilityController
import pygame
import random
import os
import time

from pygame.locals import (
    K_UP,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 650
green = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Player, self).__init__()
        self.surf = pygame.Surface((62,55), pygame.SRCALPHA)
        self.surf.blit(image, (0,0))
        self.surf.convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.move_ip(90,SCREEN_HEIGHT//3)
        self.max_count = 5 
        self.count = 0 
        self.jumping = 0

    def update(self, pressed_keys):

        self.count -= 1

        if self.count <= 0 and (pressed_keys[K_UP] or pressed_keys[K_SPACE]):
            self.jumping = 10
            self.count = self.max_count
        
        if self.jumping > 0:
            self.rect.move_ip(0, -8)
            self.jumping -= 1
            self.count = self.max_count
        else:
            self.rect.move_ip(0,4)

        if self.rect.top <= 75:
            self.rect.top = 75

    def check_bounds(self):
        return self.rect.bottom >= (SCREEN_HEIGHT - 75)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, height, center, image, speed):
        super(Pipe, self).__init__()
        self.surf = pygame.Surface((image.get_width(), height), pygame.SRCALPHA)
        self.surf.blit(image, (0,0))
        self.rect  = self.surf.get_rect(center=center)
        self.speed = speed

    def update(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, speed):
        super(Enemy, self).__init__()
        gap = 175
        height = random.randint(125, SCREEN_HEIGHT - gap - 125)
        x_start = SCREEN_WIDTH + image.get_width()
        self.pipe_bottom = Pipe(height, (x_start, (SCREEN_HEIGHT - height / 2)), image, speed)
        self.pipe_top = Pipe(SCREEN_HEIGHT - height - gap, (x_start, (SCREEN_HEIGHT - height - gap) / 2), pygame.transform.flip(image.subsurface((0,0,image.get_width(), (SCREEN_HEIGHT -height - gap))), False, True), speed)


    def get_surfs(self):
        return self.pipe_bottom, self.pipe_top


class TextColumns:
    def __init__(self, x, numbers):

        self.font_size = 20
        self.font = pygame.font.SysFont('matrix', self.font_size)
        self.num = numbers
        self.x = x

        self.speed_max = random.randint(4,6)
        self.speed_min = random.randint(2,4)

        self.create_column()


    def blit_numbers(self, screen):

        self.speed = random.randint(self.speed_min,self.speed_max)

        if self.numbers[-1][1].top >= SCREEN_HEIGHT:
            self.create_column()

        for text, text_rect in self.numbers:
            screen.blit(text, text_rect)
            text_rect.move_ip(0,self.speed)


    def create_column(self):

        yoffset = random.randint(-160, 0)
        
        self.numbers  = []
        for i in range(self.num):
            
            text = self.font.render(str(random.randint(1,9)), True, green)
            text_rect = text.get_rect()
            text_rect.move_ip(self.x, self.font_size * (yoffset - i))
            self.numbers.append((text, text_rect))

def game():
    
    start_time = time.time()

    columns = 60 
    text_columns = []
    for i in range (columns):
        text_columns.append(TextColumns(SCREEN_WIDTH / columns * i, random.randint(130,250)))
    
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    player_image = pygame.image.load(os.path.join(os.path.dirname(__file__),"res\Brain.png"))
    obstacle_image = pygame.image.load(os.path.join(os.path.dirname(__file__),"res\Pipe.png"))
    floor_image = pygame.image.load(os.path.join(os.path.dirname(__file__),"res\Floor.png"))
    
    pygame.display.set_caption("NatHacks Flappy Brain")
    pygame.display.set_icon(player_image)

    enemy_speed = 5
    score_font = pygame.font.SysFont('matrix', 60)


    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 2500)
    running = True
    clock = pygame.time.Clock()

    player = Player(player_image)

    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    i = 0
    
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    break

            if event.type == ADDENEMY:
                new_enemy = Enemy(obstacle_image, enemy_speed)
                enemies.add(new_enemy.get_surfs())
                all_sprites.add(new_enemy.get_surfs())

        screen.fill((0,0,0))
        

        for tc in text_columns:
            tc.blit_numbers(screen)

        i += enemy_speed

        if i == floor_image.get_width(): 
            i = 0

        for x in range(0, SCREEN_WIDTH + floor_image.get_width() * 2, floor_image.get_width()):
            screen.blit(floor_image, (x - i, SCREEN_HEIGHT - floor_image.get_height()))
            screen.blit(pygame.transform.flip(floor_image, False, True), (x - i, 0))


        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        enemies.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        player_died = player.check_bounds()

        if pygame.sprite.spritecollideany(player, enemies) or player_died:
            player.kill() 
            running = False

        score = str(int(2*(time.time() - start_time)))
        score_text = score_font.render(score, True, green)
        score_text_rect = score_text.get_rect(center = (SCREEN_WIDTH/2, 30))

        
        screen.blit(score_text, score_text_rect)
        pygame.display.flip()
        clock.tick(30)
    
    return score

def menu(score):

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.fill('black')
    running = True

    font = pygame.font.SysFont('matrix', 60)
    title_text = font.render("Your Score!", False, "green")
    title_rect = title_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5))
    screen.blit(title_text, title_rect)

    cont_text = font.render("Press Space to Play Again", False, "green")
    cont_rect = cont_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 // 3))
    screen.blit(cont_text, cont_rect)

    score_font = pygame.font.SysFont('matrix', 120)
    score_text = score_font.render(str(score), False, "green")
    score_rect = score_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
    screen.blit(score_text, score_rect)


    pygame.display.flip()

    while running:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return False

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return False

            if event.type == KEYDOWN and event.key == K_SPACE:
                return True
                    

        


if __name__ == "__main__":
    
    pygame.init()

    score = game()

    cont = True
    while cont: 
        cont = menu(score)
        if cont:
            score = game()

    pygame.quit()