import pygame
import data.constants as c
import math
from data.turret_data import TURRET_DATA

class Turret(pygame.sprite.Sprite):
    def __init__(self, tile_x, tile_y, data, id, sfx_shot):
        pygame.sprite.Sprite.__init__(self)
        self.data = data
        self.id = id
        self.sfx_shot = sfx_shot
        self.level = 1
        self.sprite_sheet = pygame.image.load(self.data[self.level - 1].get('path')).convert_alpha()
        self.anim_list = self.load_images()
        self.frame = 0
        self.ori_image = self.anim_list[self.frame]
        self.angle = 90
        self.image = pygame.transform.rotate(self.ori_image, self.angle)
        self.update_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()

        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (tile_x + 0.5) *  c.TILE_SIZE
        self.y = (tile_y + 0.5) *  c.TILE_SIZE
        self.pos = (self.x, self.y)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.range = self.data[self.level - 1].get('range')
        self.damage = self.data[self.level - 1].get('damage')
        self.cooldown = self.data[self.level - 1].get('cooldown')
        
        self.range_image = pygame.Surface((self.range * 2, self.range *2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, 'grey100', (self.range, self.range) , self.range)
        self.range_image.set_alpha(80)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

        self.selected = False
        self.target = None
        self.preview_img = self.anim_list[0]


    def load_images(self):
        size = self.sprite_sheet.get_height()
        anim_list = []
        for x in range(c.ANIM_STEPS):
            image = self.sprite_sheet.subsurface( x * size, 0, size, size)
            anim_list.append(image)
        return anim_list

    def upgrade(self):
        self.level = min(self.level + 1, 4)
        self.range = self.data[self.level - 1].get('range')
        self.damage = self.data[self.level - 1].get('damage')
        self.cooldown = self.data[self.level - 1].get('cooldown')

        self.sprite_sheet = self.sprite_sheet = pygame.image.load(self.data[self.level - 1].get('path')).convert_alpha()
        self.anim_list = self.load_images()
        self.ori_image = self.anim_list[self.frame]
        self.preview_img = self.anim_list[0]

        self.range_image = pygame.Surface((self.range * 2, self.range *2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, 'grey100', (self.range, self.range) , self.range)
        self.range_image.set_alpha(80)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
        

    def update(self, enemy_group, world):
        
        if pygame.time.get_ticks() - self.last_shot > self.cooldown / world.game_speed:
            self.pick_target(enemy_group)
            if self.target:
                self.play_anim() 
            
            
    def pick_target(self, enemy_group):
        found_enemy = False
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist <= self.range:
                    found_enemy = True
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))                   
                    break
        if found_enemy == False:
            self.frame = 0
            self.ori_image = self.anim_list[self.frame]
            self.target = None       

    
    def draw(self, suf):
        if self.target:
            x_dist = self.target.pos[0] - self.x
            y_dist = self.target.pos[1] - self.y
            self.angle = math.degrees(math.atan2(-y_dist, x_dist))
        self.image = pygame.transform.rotate(self.ori_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        suf.blit(self.image, self.rect)
        if self.selected == True:
            suf.blit(self.range_image, self.range_rect)

    def play_anim(self):
        self.ori_image = self.anim_list[self.frame]
        if pygame.time.get_ticks() - self.update_time > c.ANIM_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
            if(self.frame >= len(self.anim_list)):
                self.frame = 0
                self.target.health -= self.damage
                self.sfx_shot.play()
                self.last_shot = pygame.time.get_ticks()
                

    