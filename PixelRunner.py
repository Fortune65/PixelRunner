import pygame
import random
from sys import exit
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly' and level == 1:
            fly_1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        if type == 'snail' and level == 1:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        if type == 'fly' and level == 2:
            fly_1 = pygame.image.load('graphics/Fly/flyFly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/flyFly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        if type == 'snail' and level == 2:
            snail_1 = pygame.image.load('graphics/Slime/slimeWalk1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/Slime/slimeWalk2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        if score >= 20:
            self.rect.x -= 6.25
        if score >= 40:
            self.rect.x -= 6.75
        if score >= 80:
            self.rect.x -= 7.3
        if score >= 135:
            self.rect.x -= 8
        if score >= 200:
            self.rect.x -= 9
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    global score_surf, score_rect
    global previous_score_surf, previous_score_rect
    global high_score_surf, high_score_rect
    global level_surf, level_rect
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False, (64,64,64))
    score_rect = score_surf.get_rect(center=(390,50))
    previous_score_surf = test_font.render(f'Previous Score: {previous_score}',False, (64,64,64))
    previous_score_rect = previous_score_surf.get_rect(center=(400,80))
    high_score_surf = test_font.render(f'High Score: {high_score}',False, (64, 64, 64))
    high_score_rect = high_score_surf.get_rect(center=(400, 110))
    level_surf = test_font.render(f'Level: {level}', False, (64, 64, 64))
    level_rect = level_surf.get_rect(center=(700, 50))
    score_surf = pygame.transform.rotozoom(score_surf, 0, 0.9)
    previous_score_surf = pygame.transform.rotozoom(previous_score_surf, 0, 0.9)
    high_score_surf = pygame.transform.rotozoom(high_score_surf, 0, 0.9)
    level_surf = pygame.transform.rotozoom(level_surf, 0, 0.9)
    screen.blit(score_surf, score_rect)
    screen.blit(previous_score_surf, previous_score_rect)
    screen.blit(high_score_surf, high_score_rect)
    screen.blit(level_surf, level_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True


def level_two():
    level_two_bg = pygame.image.load('graphics/bg_shroom.png')
    screen.blit(level_two_bg, (0,-50))
    screen.blit(ground_surface, (0,300))
    screen.blit(score_surf, score_rect)
    screen.blit(previous_score_surf, previous_score_rect)
    screen.blit(high_score_surf, high_score_rect)
    screen.blit(level_surf, level_rect)


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0
previous_score = 0
with open('high_score.txt', 'r') as file:
    high_score = file.read()
    file.close()
level = 1
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops= -1)
bg_music.set_volume(0.2)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

level_up_surf = test_font.render("YOU REACHED LEVEL TWO!",False,(64,64,64))
level_up_rect = level_up_surf.get_rect(center=(400,150))
level_up_surf = pygame.transform.rotozoom(level_up_surf, 0, 0.9)


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                previous_score = score
                if str(score) > str(high_score):
                    high_score = int(score)
                    with open('high_score.txt', 'w') as file:
                        file.write(str(high_score))
                        file.close()
                level = 1
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        if score >= 20:
            level_two()
            level = 2
            if score >= 20 and score <= 22:
                screen.blit(level_up_surf, level_up_rect)
                obstacle_group.empty()


        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
