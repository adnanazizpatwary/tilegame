import pickle
from os import path
# import green as green
import pygame
from pygame.locals import *
pygame.init()

clk = pygame.time.Clock()
fps = 60
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("adnan")
font_score = pygame.font.SysFont('Bauhaus 93',30)

tile_Size = 30
game_over =0
main_menu = True
level = 0
max_levels = 6
score = 0
green=(0,255,0)

sun_img = pygame.image.load('sun.png')
bg_img = pygame.image.load('sky.png')
restart_img = pygame.image.load('restart_btn.png')
star_img = pygame.image.load('start_btn.png')
exit_img = pygame.image.load('exit_btn.png')
def draw_grid():
    for line in range(0,20):
        pygame.draw.line(screen,(255,255,255),(0,line*tile_Size),(screen_width,line * tile_Size))
        pygame.draw.line(screen,(255,255,255),(line*tile_Size,0),(line*tile_Size,screen_height))
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
def reset_level(level):
    player.reset(60, screen_height - 110)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clickd = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] ==1 and self.clickd == False:
                self.clickd = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clickd = False

        screen.blit(self.image,self.rect)
        return action
class Player():

    def __init__(self,x,y):
        self.reset(x,y)
    def update(self,game_over):
        dx=0
        dy=0
        walk_cooldown = 5


        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air ==False:
                self.vel_y = -20
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx-=6
                self.counter +=1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx+=6
                self.counter +=1
                self.direction= 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            # self.counte +=1
            if self.counter > walk_cooldown:
                self.counter =0
                self.index +=1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image=self.images_right[self.index]
                if self.direction == -1:
                    self.image=self.images_left[self.index]

            self.vel_y +=1
            if self.vel_y >10:
                self.vel_y =10
            dy += self.vel_y

            self.in_air =True

            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                    dx=0
                if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                    if self.vel_y <0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >=0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y =0
                        self.in_air = False

            if pygame.sprite.spritecollide(self,blob_group,False):
                game_over = -1

            if pygame.sprite.spritecollide(self,lava_group,False):
                game_over = -1
            if pygame.sprite.spritecollide(self,exit_group,False):
                game_over = 1

            self.rect.x +=dx
            self.rect.y +=dy

        elif game_over == -1:
            self.image =self.dead_image
            if self.rect.y>100:
                self.rect.y -=5



        screen.blit(self.image,self.rect)
        # pygame.draw.rect(screen,(255,255,255),self.rect,2)
        return game_over
    def reset(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for n in range(1, 5):
            img_right = pygame.image.load(f'guy{n}.png')
            img_right = pygame.transform.scale(img_right, (25, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
class World():
    def __init__(self,data):
        self.tile_list = []
        dirt_img = pygame.image.load('dirt.png')
        grass_img = pygame.image.load('grass.png')
        row_count=0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_Size,tile_Size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_Size
                    img_rect.y = row_count * tile_Size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_Size,tile_Size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_Size
                    img_rect.y = row_count * tile_Size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile ==3:
                    blob = Enenmy(col_count*tile_Size,row_count*tile_Size+1)
                    blob_group.add(blob)
                if tile == 6:
                    lava = Lava(col_count*tile_Size,row_count*tile_Size+(tile_Size/2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count*tile_Size+(tile_Size//2),row_count*tile_Size+(tile_Size/2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count*tile_Size,row_count*tile_Size-(tile_Size//2))
                    exit_group.add(exit)
                col_count += 1
            row_count +=1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen,(255,255,255),tile[1],2)
class Enenmy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('blob.png')
        self.image = pygame.transform.scale(img,(20,30))
        self.rect = self.image.get_rect()
        # image_blob = pygame.transform.scale(self.image,(10,20))
        self.rect.x = x
        self.rect.y = y
        self.move_direction =1
        self.move_counter =0
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) >50:
            self.move_direction *=-1
            self.move_counter *=-1
class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('lava.png')
        self.image = pygame.transform.scale(img,(tile_Size,tile_Size//2))
        self.rect = self.image.get_rect()
        # image_blob = pygame.transform.scale(self.image,(10,20))
        self.rect.x = x
        self.rect.y = y
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(img,(tile_Size//2,tile_Size//2))
        self.rect = self.image.get_rect()
        # image_blob = pygame.transform.scale(self.image,(10,20))
        self.rect.center = (x,y)


class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('exit.png')
        self.image = pygame.transform.scale(img,(tile_Size,int(tile_Size*1.5)))
        self.rect = self.image.get_rect()
        # image_blob = pygame.transform.scale(self.image,(10,20))
        self.rect.x = x
        self.rect.y = y






player = Player(60, screen_height-110)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data','rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)
restart_button = Button(screen_width//2-27,screen_height//2+62,restart_img)
start_button = Button(screen_width//2-250,screen_height//2,star_img)
exit_button = Button(screen_width//2+60,screen_height//2,exit_img)

run = True
while run:
    clk.tick(fps)

    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,(30, 30))
    if main_menu ==True:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False

    else:

        world.draw()
        if game_over == 0:
            blob_group.update()
            if pygame.sprite.spritecollide(player,coin_group,True):
                score+=10
            draw_text('X '+ str(score),font_score,green,tile_Size-10,0)
        blob_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        game_over = player.update(game_over)
        if game_over == -1:
            if restart_button.draw():
                player.reset(60, screen_height - 110)
                game_over =0
                score =0
        if game_over == 1:
            level +=1
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over= 0
            else:
                if restart_button.draw():
                    level = 0
                    world_data =[]
                    world = reset_level(level)
                    game_over = 0
                    score = 0
    # draw_grid()
    # print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()





