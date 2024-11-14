import pygame
import data.constants as c
import math
from pygame.math import Vector2
from data.enemy_data import ENEMY_DATA


path = 'data/assets/images/enemies/'

class Enemy(pygame.sprite.Sprite):
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.waypoints = self.world.waypoints
        self.level = self.world.enemy_list[self.world.spawned_enemy]
        
        self.pos = Vector2(self.waypoints[0])
        self.original_image = pygame.image.load(path + 'map_' + str(self.world.map_number) + '_level_' + self.level + '.png').convert_alpha()
        self.target_waypoint = 1
        self.health = ENEMY_DATA['map_' + str(self.world.map_number)][self.level].get('health')
        self.speed = ENEMY_DATA['map_' + str(self.world.map_number)][self.level].get('speed')
        self.reward = self.health
        self.movement = (0,0)
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, clock):

        if self.health <= ENEMY_DATA['map_' + str(self.world.map_number)][str(max(1, int(self.level) - 1))].get('health'):
            self.level = str(max(1, int(self.level) - 1))
            self.original_image = pygame.image.load(path + 'map_' + str(self.world.map_number) + '_level_' + self.level + '.png').convert_alpha()

        self.rotate()
        self.move(clock)
        self.check_alive()

    def rotate(self):
        self.target = Vector2(self.waypoints[self.target_waypoint])
        #calculate distance to next waypoint
        dist = self.target - self.pos
        #use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotate image and update rectangle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move(self, clock):
        
        self.movement = self.target - self.pos
        dist = self.movement.length()
        if dist >= 1 / clock.get_fps() * (self.speed * 60) * self.world.game_speed:
            self.pos += self.movement.normalize() / clock.get_fps() * (self.speed * 60) * self.world.game_speed
        elif dist > 0: 
            self.pos += self.movement.normalize() * dist
        else:
            self.target_waypoint += 1
            if(self.target_waypoint == len(self.waypoints)):
                self.kill()
                self.world.health = max(0, self.world.health - self.health)
                
        self.rect.center = self.pos

    def check_alive(self):
        if self.health <= 0:
            self.kill()
            self.world.money += self.reward