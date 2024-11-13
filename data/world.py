import pygame
import random
import json

import data.constants as c
from data.enemy_data import ENEMY_SPAWN_DATA

class World:
    def __init__(self, map_number):
        self.map_number = map_number
        self.map_data = json.load(open('data/levels/map_' + str(map_number) + '.tmj'))
        self.image = pygame.transform.scale(pygame.image.load('data/levels/map_' + str(map_number) +'.png'), (c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        
        self.waypoints = []
        self.tile_map = []
        self.enemy_list = []
        self.spawned_enemy = 0
        self.round_reward = 0
        self.game_speed = 1
        self.round = 1
        self.round_nums = len(ENEMY_SPAWN_DATA["map_" + str(self.map_number)])
        self.health = 100
        self.money = 800
        self.process_data()
        self.process_enemies()

    def process_data(self):
        for layer in self.map_data['layers']:
            if layer['name'] == 'Ground':
                self.tile_map = layer['data']

            elif layer['name'] == 'waypoints':
                for obj in layer['objects']:
                    waypoints_data = obj['polyline']
                    self.process_waypoints(waypoints_data, offset = (obj['x'], obj['y']))
                
    
    def process_enemies(self):
        self.enemy_list.clear()
        enemies = ENEMY_SPAWN_DATA["map_" + str(self.map_number)][self.round - 1]
        self.spawn_cooldown = enemies['delay']
        self.round_reward = enemies['reward']
        for enemy_rank in enemies:
            if(enemy_rank != 'delay' and enemy_rank != 'reward'):
                enemies_quantity = enemies[enemy_rank]
                for i in range(enemies_quantity):
                    self.enemy_list.append(enemy_rank)
            
        random.shuffle(self.enemy_list)
        

    def process_waypoints(self, waypoints_data, offset = (0,0)):
        for point in waypoints_data:
            self.waypoints.append((point.get('x') + offset[0], point.get('y') + offset[1]))

    def draw(self, suf):
        suf.blit(self.image, (0,0))

    def completed_round(self, enemy_group):
        if len(enemy_group) == 0:
            self.money += self.round_reward
            return True
        return False
        