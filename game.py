import pygame
import os
import json
import ctypes

os.environ['SDL_VIDEO_CENTERED'] = '1' # Set the environment variable to center the window
# ctypes.windll.user32.SetProcessDPIAware() # Turn off DPI Scaling of Window

ctypes.windll.shcore.SetProcessDpiAwareness(2)

import data.constants as c
from data.enemy import Enemy
from data.world import World
from data.turrets import Turret
from data.buttons import Button
from data.turret_data import TURRET_DATA, TURRET_TYPE

#init 
pygame.init()

#Display
screen = pygame.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
full_screen = False

pygame.display.set_caption('Tower Defense Game')

#Load map data

# map_1_image = pygame.transform.scale(pygame.image.load('data/levels/map_1.png'),(550,300)) 
# map_2_image = pygame.transform.scale(pygame.image.load('data/levels/testmap.png'),(550,300)) 

world = World(1)

#enemy
enemy_group = pygame.sprite.Group()

#turret
turret_name = 'camo'
turret_type = 'bullet'

# path_preview_list = {
#     "camo": {
#         "bullet": 'data/assets/images/turrets/Camo/Weapons/weapons_1.png',   
#         "laze": 'data/assets/images/turrets/Camo/Weapons/weapons_5.png',        
#     }
# }

current_turret_id = 1
turret_group = pygame.sprite.Group()
current_turret = Turret(0,0, TURRET_DATA[turret_name][turret_type], current_turret_id, None)


#mouse
mouse_pos = (0,0)
mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
can_place = True

#variables
current_map_number = 1
game_over = False
game_result = 0 # -1 is loss & 1 is win
game_state = 'menu'
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None
upgrade_cost = 100
sell_cost = 100
round_started = False
sound_muted = False
show_fps = True
current_info_panel_rect = pygame.Rect(0,0,0,0)

last_fps = 60
max_fps = 60
delay_update_fps_time = 250
last_update_fps = pygame.time.get_ticks()
auto_fast_speed = False
music = True
sfx = True

slot_height = 120
slot_width = 80
slot_space = 10
slot_cols = 2
slot_rows = 4

dark_overlay = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 0))  # Đen với alpha 100

menu_bg = pygame.transform.scale(pygame.image.load("data/assets/images/backgrounds/menu_bg.png").convert_alpha(), (c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
slot_bg = pygame.image.load('data/assets/images/backgrounds/SlotImage.png')
preview_bg = pygame.image.load('data/assets/images/backgrounds/preview_turret.png')
arrow_right_img = pygame.image.load('data/assets/images/gui/arrow_right.png').convert_alpha()
arrow_right_img = pygame.transform.scale(arrow_right_img, (100,76))
slot_buttons = []
#create slot buttons
for y in range(15, (10 + slot_space + slot_height)*(slot_rows - 1) + 1, slot_height + slot_space):
    slot_buttons.append(Button(c.SCREEN_WIDTH + 5, y, dark_overlay, True))
    slot_buttons.append(Button(c.SCREEN_WIDTH + slot_width + slot_space + 5, y, dark_overlay, True))
    if y == 15: break

#button
new_game_image = pygame.image.load('data/assets/images/buttons/new_game.png').convert_alpha()
choose_level_image = pygame.image.load('data/assets/images/buttons/choose_level.png').convert_alpha()
options_image = pygame.image.load('data/assets/images/buttons/options.png').convert_alpha()
exit_game_image = pygame.image.load('data/assets/images/buttons/exit.png').convert_alpha()
arrow_navigation_right_img = pygame.image.load('data/assets/images/buttons/arrow_right.png').convert_alpha()
arrow_navigation_left_img = pygame.image.load('data/assets/images/buttons/arrow_left.png').convert_alpha()
buy_turret_image = pygame.image.load('data/assets/images/buttons/buy_turret.png').convert_alpha()
sell_image = pygame.image.load('data/assets/images/buttons/sell.png').convert_alpha()
green_button_img = pygame.transform.scale(pygame.image.load('data/assets/images/buttons/green_button.png').convert_alpha(), (200, 90))
sample_button_img = pygame.image.load('data/assets/images/buttons/sample.png').convert_alpha()
preview_map_img = pygame.transform.scale(pygame.image.load('data/levels/map_' + str(current_map_number) + '.png').convert_alpha(),(550,300))
exit_icon_img = pygame.image.load('data/assets/images/buttons/exit_icon.png').convert_alpha()
setting_icon_img = pygame.transform.scale(pygame.image.load('data/assets/images/buttons/setting.png').convert_alpha(), (85, 80))
mute_icon_img = pygame.transform.scale(pygame.image.load('data/assets/images/buttons/mute_icon.png').convert_alpha(), (65, 65))
unmute_icon_img = pygame.transform.scale(pygame.image.load('data/assets/images/buttons/unmute_icon.png').convert_alpha(), (65, 65))



#GUI
heart_image = pygame.image.load("data/assets/images/gui/heart.png").convert_alpha()
coin_image = pygame.image.load("data/assets/images/gui/coin.png").convert_alpha()
damage_img = pygame.transform.scale(pygame.image.load("data/assets/images/gui/damage_icon.png").convert_alpha(), (39,36))
range_img = pygame.transform.scale(pygame.image.load("data/assets/images/gui/range_icon.png").convert_alpha(), (36,36))
speed_img = pygame.transform.scale(pygame.image.load("data/assets/images/gui/speed_icon.png").convert_alpha(), (44,44))

#create button
new_game_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - new_game_image.get_width() / 2, 330, new_game_image, True)
choose_level_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - choose_level_image.get_width() / 2, 430, choose_level_image, True)
options_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - options_image.get_width() / 2, 530, options_image, True)
exit_game_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - exit_game_image.get_width() / 2, 630, exit_game_image, True)
arrow_navigation_left_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 400, 300, pygame.transform.scale(arrow_navigation_left_img, (100,76)), True)
arrow_navigation_right_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2  + 300, 300, pygame.transform.scale(arrow_navigation_right_img, (100,76)), True)
increase_fps_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2  + 140, 230, pygame.transform.scale(arrow_navigation_right_img, (80,40)), True)
decrease_fps_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2  - 230, 230, pygame.transform.scale(arrow_navigation_left_img, (80,40)), True)

buy_turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 12, c.SCREEN_HEIGHT - 140, pygame.transform.scale(sample_button_img, (180, 74)), True)
upgrade_button = Button(c.SCREEN_WIDTH - 190, c.SCREEN_HEIGHT - 280, pygame.transform.scale(sample_button_img, (180, 74)), True)
sell_button = Button(c.SCREEN_WIDTH - 190, c.SCREEN_HEIGHT - 200, pygame.transform.scale(sample_button_img, (180, 74)), True)
begin_button = Button(c.SCREEN_WIDTH + 12, c.SCREEN_HEIGHT - 80, pygame.transform.scale(sample_button_img, (180, 74)), True)
fast_speed_button = Button(c.SCREEN_WIDTH + 12, c.SCREEN_HEIGHT - 80, pygame.transform.scale(sample_button_img, (180, 74)), True)
low_speed_button = Button(c.SCREEN_WIDTH + 12, c.SCREEN_HEIGHT - 80, pygame.transform.scale(sample_button_img, (180, 74)), True)
# sell_button = Button(c.SCREEN_WIDTH - 190, c.SCREEN_HEIGHT - 190, sell_image, True)
play_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 510, sample_button_img, True)
exit_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 + 365, 105, exit_icon_img, True)
setting_button = Button(1065, 0, setting_icon_img, True)
mute_button = Button(1073, 80, mute_icon_img, True)
unmute_button = Button(1073, 80, unmute_icon_img, True)
menu_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 470, sample_button_img, True)
menu_button_2 = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 380, sample_button_img, True)
continue_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 200, sample_button_img, True)
restart_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 380, sample_button_img, True)
restart_button_2 = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 280, sample_button_img, True)
next_level_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 280, sample_button_img, True)
show_fps_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 290, sample_button_img, True)
hide_fps_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - sample_button_img.get_width() / 2, 290, sample_button_img, True)
auto_fast_speed_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 70, 290, pygame.transform.scale(sample_button_img, (140, 74)), True)
music_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 70, 370, pygame.transform.scale(sample_button_img, (140, 74)), True)
sfx_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 70, 450, pygame.transform.scale(sample_button_img, (140, 74)), True)

#text
text_font = pygame.font.Font("data/fonts/SparkyStonesRegular-BW6ld.ttf", 24)
medium_font = pygame.font.Font("data/fonts/SparkyStonesRegular-BW6ld.ttf", 30)
large_font = pygame.font.Font("data/fonts/SparkyStonesRegular-BW6ld.ttf", 36)
huge_font = pygame.font.Font("data/fonts/SparkyStonesRegular-BW6ld.ttf", 64)

#load sounds
pygame.mixer.init()

bg_music = pygame.mixer.Sound('data/assets/audio/background_music.mp3')
bg_music.set_volume(0.3)
bg_music.play(-1)

game_music = pygame.mixer.Sound('data/assets/audio/game_music.mp3')
game_music.set_volume(0.2)
# game_music.play(-1)

sfx_shot = pygame.mixer.Sound('data/assets/audio/shot.wav')
sfx_shot.set_volume(0.5)

# Method
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_text_with_outline(text, font, text_color, outline_color, outline_width, x , y, center = False):
    # Render the outline by rendering the text multiple times with a small offset
    outline_surfaces = []
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                outline_surfaces.append((outline_surface, (dx, dy)))
    
    # Render the main text
    text_surface = font.render(text, True, text_color)
    
    # Create a new surface large enough to hold both text and outline
    surface = pygame.Surface((text_surface.get_width() + outline_width * 2, 
                              text_surface.get_height() + outline_width * 2), 
                              pygame.SRCALPHA)
    
    # Blit all outline surfaces onto the new surface
    for outline_surface, offset in outline_surfaces:
        surface.blit(outline_surface, (outline_width + offset[0], outline_width + offset[1]))
    
    # Blit the main text onto the new surface
    surface.blit(text_surface, (outline_width, outline_width))
    
    if center == True:
        surface_rect = surface.get_rect()
        surface_rect.center = (x,y)
        screen.blit(surface, surface_rect)
    else:
        screen.blit(surface, (x,y))

def create_turret():
    global placing_turrets
    buy_cost = TURRET_TYPE[current_turret_id]['cost']

    if(world.money >= buy_cost):
        current_turret = Turret(mouse_tile_x, mouse_tile_y, TURRET_DATA[TURRET_TYPE[current_turret_id]['name']][TURRET_TYPE[current_turret_id]['type']], current_turret_id, sfx_shot)
        turret_group.add(current_turret)
        world.money -= buy_cost
        placing_turrets = False

def select_turret():
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
            
def clear_selection():
    for turret in turret_group:
        turret.selected = False

def draw_preview_turret():
    base_range = TURRET_TYPE[current_turret_id]['base_range']

    range_image = pygame.Surface((base_range * 2, base_range * 2), pygame.SRCALPHA)
    range_image.set_alpha(0.3 * 255)

    if can_place == True:
        pygame.draw.circle(range_image, 'white', (base_range , base_range), base_range)
        screen.blit(range_image, (mouse_pos[0] - base_range, mouse_pos[1] - base_range))
    else:
        pygame.draw.circle(range_image, 'red', (base_range , base_range), base_range)
        screen.blit(range_image, (mouse_pos[0] - base_range, mouse_pos[1] - base_range))
    
    preview_turret_image = pygame.image.load(TURRET_TYPE[current_turret_id]['path']).convert_alpha()
    preview_turret_image.set_alpha(0.4 * 255)
    screen.blit(preview_turret_image, (mouse_pos[0] - c.TILE_SIZE, mouse_pos[1] - c.TILE_SIZE))
    # preview_turret_image.set_alpha(255)


def spawn_enemy():
    global round_started
    global last_enemy_spawn
    if pygame.time.get_ticks() - last_enemy_spawn > world.spawn_cooldown / world.game_speed:       
        if world.spawned_enemy < len(world.enemy_list):
            enemy = Enemy(world) 
            enemy_group.add(enemy)
            world.spawned_enemy += 1
        elif world.completed_round(enemy_group):                                   
            world.spawned_enemy = 0
            round_started = False
            world.round += 1
            if(world.round <= world.round_nums):
                world.process_enemies()
  
        last_enemy_spawn = pygame.time.get_ticks()

def display_data():
    global placing_turrets
    global current_turret_id
    #draw panel
    pygame.draw.rect(screen, (187, 147, 95), (c.SCREEN_WIDTH - 10, 0, c.SIDE_PANEL + 20, c.SCREEN_HEIGHT), border_radius=15)
    pygame.draw.rect(screen, (139, 94, 55), (c.SCREEN_WIDTH - 10, 0, c.SIDE_PANEL + 20, c.SCREEN_HEIGHT), 4, border_radius=15)

    slot_created = 0
    cost_text_col = 'white'
    #draw slot tile
    for y in range(15, (10 + slot_space + slot_height)*(slot_rows - 1) + 1, slot_height + slot_space):
        
        # pygame.draw.rect(screen, (149, 102, 58), (c.SCREEN_WIDTH + 5, y, slot_width, slot_height))
        # pygame.draw.rect(screen, (149, 102, 58), (c.SCREEN_WIDTH + slot_width + slot_space + 5, y, slot_width, slot_height))

        slot_created += 1
        if world.money >= TURRET_TYPE[slot_created]['cost']:
            cost_text_col = 'white'
        else: cost_text_col  = 'red'

        screen.blit(slot_bg, (c.SCREEN_WIDTH + 5, y))
        pygame.draw.rect(screen, (111, 74, 43), (c.SCREEN_WIDTH + 5 , y, slot_width , slot_height ), 2)
        turret_preview = pygame.image.load(TURRET_TYPE[slot_created]['path']).convert_alpha()
        turret_preview_rect = turret_preview.get_rect()
        turret_preview_rect.center = (c.SCREEN_WIDTH + 5 + slot_width / 2, y + slot_height / 2)
        screen.blit(turret_preview, turret_preview_rect)
        
        if(world.money >= TURRET_TYPE[slot_created]['cost']):
            slot_buttons[0].image.fill((0,0,0,0))         
            if slot_buttons[0].draw(screen):
                placing_turrets = True
                current_turret_id = slot_created
        else:
            slot_buttons[0].image.fill((0,0,0,100))
            slot_buttons[0].draw(screen)       
        draw_text_with_outline('$' + str(TURRET_TYPE[slot_created]['cost']), text_font, cost_text_col, 'black', 1, c.SCREEN_WIDTH + 5 + slot_width / 2, y + slot_height * 5 / 6, center=True)
        
        slot_created += 1    
        if world.money >= TURRET_TYPE[slot_created]['cost']:
            cost_text_col = 'white'
        else: cost_text_col  = 'red'
        screen.blit(slot_bg, (c.SCREEN_WIDTH + slot_width + slot_space + 5, y))
        pygame.draw.rect(screen, (111, 74, 43), (c.SCREEN_WIDTH + slot_width + slot_space + 5 , y, slot_width , slot_height ), 2)
        turret_preview = pygame.image.load(TURRET_TYPE[slot_created]['path']).convert_alpha()
        turret_preview_rect = turret_preview.get_rect()
        turret_preview_rect.center = (c.SCREEN_WIDTH + slot_width + slot_space + 5 + slot_width / 2, y + slot_height / 2)
        screen.blit(turret_preview, turret_preview_rect)

        if(world.money >= TURRET_TYPE[slot_created]['cost']):
            slot_buttons[1].image.fill((0,0,0,0))         
            if slot_buttons[1].draw(screen):
                placing_turrets = True
                current_turret_id = slot_created
        else:
            slot_buttons[1].image.fill((0,0,0,100))
            slot_buttons[1].draw(screen)
        draw_text_with_outline('$' + str(TURRET_TYPE[slot_created]['cost']), text_font, cost_text_col, 'black', 1, c.SCREEN_WIDTH + slot_width + slot_space + 5 + slot_width / 2, y + slot_height * 5 / 6, center= True)

        if(slot_created == 2): break
    

    #display data
    draw_text_with_outline("ROUND", text_font, "grey100", 'black', 1, c.SCREEN_WIDTH - 115, 25, center=True)
    draw_text_with_outline(str(min(world.round, world.round_nums)) + '/' + str(world.round_nums), large_font, "grey100", 'black', 2, c.SCREEN_WIDTH - 115, 55, center=True)
    screen.blit(heart_image, (0, 15))
    draw_text_with_outline(str(world.health), large_font, "white", 'black', 2, 35, 15)
    screen.blit(coin_image, (150, 15))
    draw_text_with_outline('$' + str(world.money), large_font, "white", 'black', 2, 185, 13)

    #return

def reset_level():
    global game_over
    global round_started
    global placing_turrets
    global selected_turret
    global last_enemy_spawn
    global world

    #Reset level
    game_over = False
    round_started = False
    placing_turrets = False
    selected_turret = None
    last_enemy_spawn = pygame.time.get_ticks()
    world = World(current_map_number)

    #empty groups
    enemy_group.empty()
    turret_group.empty()

def set_music_volume(volume):
    global game_music
    global bg_music

    game_music.set_volume(volume * 0.2)
    bg_music.set_volume(volume * 0.3)

def set_sfx_volume(volume):
    global sfx_shot

    sfx_shot.set_volume(volume * 0.5)

# 0 means no menu has been selected
# 1 is New Game
# 2 is Choose level
# 3 is Options
# 4 is Exit
choosing_menu_index = 0

clock = pygame.time.Clock()
run = True
#GAME LOOP
while run:
    clock.tick(max_fps)

    if game_state == 'menu':

        screen.blit(menu_bg, (0,0))

        if (choosing_menu_index == 0 and new_game_button.draw(screen)):
            # choosing_menu_index = 1  
            current_map_number = 1
            world = World(current_map_number)

            # switch music
            bg_music.stop()
            game_music.play(-1)
            game_state = 'playing'
            # pygame.time.delay(200) # quick fix overlap button
            

        elif choosing_menu_index == 2 or (choosing_menu_index == 0 and choose_level_button.draw(screen)):
            if choosing_menu_index == 0:
                preview_map_img = pygame.transform.scale(pygame.image.load('data/levels/map_' + str(current_map_number) + '.png'),(550,300))
            choosing_menu_index = 2

            pygame.draw.rect(screen, (187, 147, 95), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 900 / 2, 100, 900, 500), 0, 10)
            pygame.draw.rect(screen, (139, 94, 55), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 900 / 2, 100, 900, 500), 6, 10)
            
            screen.blit(preview_map_img, ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - preview_map_img.get_width() / 2, 170))
            pygame.draw.rect(screen, (139, 94, 55), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - preview_map_img.get_width() / 2 - 4, 170 - 4, 550 + 8, 300 + 8), 4, 6)
            draw_text_with_outline('MAP ' + str(current_map_number), large_font, 'white', 'black', 2, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 500, center= True)

            if current_map_number > 1 and arrow_navigation_left_button.draw(screen):
                current_map_number -= 1
                preview_map_img = pygame.transform.scale(pygame.image.load('data/levels/map_' + str(current_map_number) + '.png'),(550,300))
            if current_map_number < c.TOTAL_LEVELS and arrow_navigation_right_button.draw(screen):        
                current_map_number += 1
                preview_map_img = pygame.transform.scale(pygame.image.load('data/levels/map_' + str(current_map_number) + '.png'),(550,300))
            
            if play_button.draw(screen):
                world = World(current_map_number)
                # switch music
                bg_music.stop()
                game_music.play(-1)
                game_state = 'playing'
                # pygame.time.delay(200) # quick fix overlap button
                

            draw_text_with_outline('PLAY', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 555, center= True)

            if exit_button.draw(screen):
                choosing_menu_index = 0
                current_map_number = 1
        elif choosing_menu_index == 3 or (choosing_menu_index == 0 and options_button.draw(screen)):
            choosing_menu_index = 3

            pygame.draw.rect(screen, (187, 147, 95), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 900 / 2, 100, 900, 500), 0, 10)
            pygame.draw.rect(screen, (139, 94, 55), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 900 / 2, 100, 900, 500), 6, 10)
            draw_text_with_outline('OPTIONS', huge_font, 'white', 'black', 2, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 150, center= True)
            draw_text_with_outline('MAX FPS:', large_font, 'white', 'black', 1, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 420 , 230, center= False)
            draw_text_with_outline('AUTO FAST SPEED:', large_font, 'white', 'black', 1, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 420 , 310, center= False)
            draw_text_with_outline('MUSIC:', large_font, 'white', 'black', 1, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 420 , 390, center= False)
            draw_text_with_outline('SFX:', large_font, 'white', 'black', 1, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 420 , 470, center= False)
            

            if max_fps <= 120 and increase_fps_button.draw(screen):
                if max_fps == 120:
                    max_fps = 1000
                else: 
                    max_fps += 30
            if max_fps > 30 and decrease_fps_button.draw(screen):
                max_fps = min(120, max_fps - 30)

            if auto_fast_speed_button.draw(screen):
                auto_fast_speed = not auto_fast_speed          
            if music_button.draw(screen):
                music = not music
                set_music_volume(1 if music else 0)
                         
            if sfx_button.draw(screen):
                sfx = not sfx
                set_sfx_volume(1 if sfx else 0)
                
            
            if max_fps <= 120:
                draw_text_with_outline(str(max_fps), large_font, 'white', 'black', 1, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 250, center= True)
            else:
                draw_text_with_outline('UNLIMITED', large_font, 'white', 'black', 1, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 250, center= True)

            if auto_fast_speed:
                draw_text_with_outline('ON', medium_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 327, center= True)
            else:
                draw_text_with_outline('OFF', medium_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 327, center= True)

            if music:
                draw_text_with_outline('ON', medium_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 407, center= True)
            else:
                draw_text_with_outline('OFF', medium_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 407, center= True)
   
            if sfx:
                draw_text_with_outline('ON', medium_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 487, center= True)
            else:
                draw_text_with_outline('OFF', medium_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2, 487, center= True)

            if exit_button.draw(screen):
                choosing_menu_index = 0
                current_map_number = 1

        elif choosing_menu_index == 0 and exit_game_button.draw(screen):
            run = False

    elif game_state == 'playing':

        #draw map
        world.draw(screen)  

        if game_over == False:
            #check if player has lost
            if world.health <= 0:
                game_over = True
                game_result = -1 #loss
            #check if player has won
            if world.round > world.round_nums:
                game_over = True
                game_result = 1 #win

            #Update
            enemy_group.update(clock)
            turret_group.update(enemy_group, world)
            
        enemy_group.draw(screen)

        for turret in turret_group:
            turret.draw(screen)

        display_data()

        

        if game_over == False:
            
            if setting_button.draw(screen):
                game_state = 'setting'

            if music == True:
                if mute_button.draw(screen):
                    music = False
                    set_music_volume(0)
                    
            else:
                if unmute_button.draw(screen):
                    music = True
                    set_music_volume(1)
                    
            if round_started == False:
                if begin_button.draw(screen):
                    round_started = True  
                    world.game_speed = 4 if auto_fast_speed else 1
                draw_text_with_outline('BEGIN ROUND', text_font, (157,57,25), 'black', 0, c.SCREEN_WIDTH + 100, c.SCREEN_HEIGHT - 40, center= True)
            else:
                if world.game_speed == 1:    
                    if fast_speed_button.draw(screen):
                        world.game_speed = 4  
                    draw_text_with_outline('FAST SPEED', text_font, (157,57,25), 'black', 0, c.SCREEN_WIDTH + 100, c.SCREEN_HEIGHT - 40, center= True)
                else:
                    if low_speed_button.draw(screen):
                        world.game_speed = 1

                    draw_text_with_outline('SLOW SPEED', text_font, (157,57,25), 'black', 0, c.SCREEN_WIDTH + 100, c.SCREEN_HEIGHT - 40, center= True)

                #Spawn enemy
                spawn_enemy()
                    
            #mouse pos update
            mouse_pos = pygame.mouse.get_pos()
            mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
            mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
            mouse_tile_num = mouse_tile_y * c.COLS + mouse_tile_x
            
            #Hanlde can_place variable
            if 0 < mouse_pos[0] < c.SCREEN_WIDTH and 0 < mouse_pos[1] < c.SCREEN_HEIGHT:
                if(world.tile_map[mouse_tile_num] == 25):
                    free_space = True
                    for turret in turret_group:
                        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                            can_place = False
                            free_space = False
                            break
                    if free_space: can_place = True
                else: can_place = False 
            else: can_place = False         

            if placing_turrets == True:
                #draw preview turret
                draw_preview_turret()
                if cancel_button.draw(screen) == True:
                    placing_turrets = False
                draw_text_with_outline('CANCEL', text_font, (157,57,25), 'black', 0, c.SCREEN_WIDTH + 100, c.SCREEN_HEIGHT - 100, center= True)
                

            if selected_turret:
                #draw turret info panel
                current_info_panel_rect = pygame.draw.rect(screen, (187, 147, 95), (c.SCREEN_WIDTH - 307, c.SCREEN_HEIGHT - 700, 300, 600), border_bottom_left_radius=15, border_top_left_radius=15)
                pygame.draw.rect(screen, (139, 94, 55), (c.SCREEN_WIDTH - 307, c.SCREEN_HEIGHT - 700, 300, 600), 4, border_bottom_left_radius=15, border_top_left_radius=15)

                draw_text_with_outline(TURRET_TYPE[selected_turret.id]['type'].upper() + ' ' + TURRET_TYPE[selected_turret.id]['name'].upper(), large_font, 'white', 'black', 2, c.SCREEN_WIDTH - 153, c.SCREEN_HEIGHT - 670, center=True)

                screen.blit(preview_bg, (c.SCREEN_WIDTH - 280, c.SCREEN_HEIGHT - 650))
                pygame.draw.rect(screen, (139, 94, 55), (c.SCREEN_WIDTH - 280, c.SCREEN_HEIGHT - 650, 250, 150), 4)
                preview_img = pygame.transform.scale(selected_turret.preview_img, (192, 192))
                preview_img_rect = preview_img.get_rect()
                preview_img_rect.center = (c.SCREEN_WIDTH - 280 + 125, c.SCREEN_HEIGHT - 650 + 85)
                screen.blit(preview_img, preview_img_rect)

                #draw game state
                screen.blit(damage_img, (c.SCREEN_WIDTH - 295, c.SCREEN_HEIGHT - 472))
                screen.blit(range_img, (c.SCREEN_WIDTH - 295, c.SCREEN_HEIGHT - 472 + 40))
                screen.blit(speed_img, (c.SCREEN_WIDTH - 300, c.SCREEN_HEIGHT - 472 + 77))

                draw_text_with_outline(str(selected_turret.damage), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 255, c.SCREEN_HEIGHT - 470)
                draw_text_with_outline(str(selected_turret.range), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 255, c.SCREEN_HEIGHT - 470 + 40)
                draw_text_with_outline(str(5 - int(selected_turret.cooldown / 300) + 1), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 255, c.SCREEN_HEIGHT - 470 + 80)
                draw_text_with_outline('LV.' + str(selected_turret.level) + (' (Max)' if selected_turret.level == 4 else ''), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 270, c.SCREEN_HEIGHT - 470 + 130)

                cost_text_col = 'white'
                if selected_turret.level < 4:
                    screen.blit(arrow_right_img, (c.SCREEN_WIDTH - 190, c.SCREEN_HEIGHT - 420))

                    draw_text_with_outline(str(selected_turret.data[selected_turret.level]['damage']), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 80, c.SCREEN_HEIGHT - 470)
                    draw_text_with_outline(str(selected_turret.data[selected_turret.level]['range']), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 80, c.SCREEN_HEIGHT - 470 + 40)
                    draw_text_with_outline(str(5 - int(selected_turret.data[selected_turret.level]['cooldown'] / 300) + 1), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 80, c.SCREEN_HEIGHT - 470 + 80)
                    draw_text_with_outline('LV.' + str(selected_turret.level + 1), large_font, 'white', 'black', 1, c.SCREEN_WIDTH - 80, c.SCREEN_HEIGHT - 470 + 130)


                    #handle upgrade button
                    if upgrade_button.draw(screen):
                        if(world.money >= upgrade_cost):
                            selected_turret.upgrade()
                            world.money -= upgrade_cost
                    draw_text_with_outline('UPGRADE', medium_font, (157,57,25), 'black', 0, c.SCREEN_WIDTH - 100, c.SCREEN_HEIGHT - 240, center= True)
                    
                    if world.money >= upgrade_cost:
                        cost_text_col = 'white'
                    else: cost_text_col  = 'red'

                    draw_text_with_outline('$' + str(upgrade_cost), text_font, cost_text_col, 'black', 1,  c.SCREEN_WIDTH - 245, c.SCREEN_HEIGHT - 255)
                    screen.blit(coin_image, (c.SCREEN_WIDTH - 280, c.SCREEN_HEIGHT - 258))
                    
                #Handle sell button
                draw_text_with_outline('$' + str(sell_cost), text_font, 'white', 'black', 1,  c.SCREEN_WIDTH - 245, c.SCREEN_HEIGHT - 175)
                screen.blit(coin_image, (c.SCREEN_WIDTH - 280, c.SCREEN_HEIGHT - 178))
                if sell_button.draw(screen):
                    selected_turret.kill()
                    selected_turret = None
                    world.money += sell_cost
                draw_text_with_outline('SELL', medium_font, (157,57,25), 'black', 0, c.SCREEN_WIDTH - 100, c.SCREEN_HEIGHT - 160, center= True)
                
        else:
            pygame.draw.rect(screen, (187, 147, 95), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 400 / 2, 200, 400, 300), 0, 10)
            pygame.draw.rect(screen, (139, 94, 55), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 400 / 2, 200, 400, 300), 6, 10)

            if game_result == -1:
                draw_text_with_outline('GAME OVER!', huge_font, 'white', 'black', 2, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 250, center= True)
                #restart level
                if restart_button_2.draw(screen):
                    game_state = 'playing'
                    reset_level()
                    game_music.stop()
                    game_music.play(-1)
                draw_text_with_outline('RESTART', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 325, center= True)
                
                
            elif game_result == 1:
                draw_text_with_outline('WON!', huge_font, 'white', 'black', 2, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 250, center= True)

                if next_level_button.draw(screen):
                    game_state = 'playing'
                    current_map_number = min(c.TOTAL_LEVELS, current_map_number + 1)
                    reset_level()
                    game_music.stop()
                    game_music.play(-1)
                draw_text_with_outline('NEXT LEVEL', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 325, center= True)

            if menu_button_2.draw(screen):
                game_state = 'menu'
                current_map_number = 1
                choosing_menu_index = 0
                game_music.stop()
                bg_music.play(-1)
                reset_level()
                # pygame.time.delay(200) # quick fix overlap button
            draw_text_with_outline('MENU', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 425, center= True)
            
    
    elif game_state == 'setting':
        world.draw(screen)
        enemy_group.draw(screen)

        for turret in turret_group:
            turret.draw(screen)

        display_data()

        pygame.draw.rect(screen, (187, 147, 95), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 400 / 2, 100, 400, 500), 0, 10)
        pygame.draw.rect(screen, (139, 94, 55), ((c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 - 400 / 2, 100, 400, 500), 6, 10)
        draw_text_with_outline('SETTING', huge_font, 'white', 'black', 2, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 150, center= True)

        if menu_button.draw(screen):
            game_state = 'menu'
            current_map_number = 1
            choosing_menu_index = 0
            game_music.stop()
            bg_music.play(-1)
            reset_level()
            # pygame.time.delay(200) # quick fix overlap button

        draw_text_with_outline('MENU', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 515, center= True)

        if continue_button.draw(screen):
            game_state = 'playing'
        draw_text_with_outline('CONTINUE', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 245, center= True)

        if show_fps == False:
            if show_fps_button.draw(screen):
                show_fps = True        
            draw_text_with_outline('SHOW FPS', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 335, center= True)     
        else:
            if hide_fps_button.draw(screen):
                show_fps = False
            draw_text_with_outline('HIDE FPS', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 335, center= True)     
        



        if restart_button.draw(screen):
            game_state = 'playing'
            reset_level()
            game_music.stop()
            game_music.play(-1)

        draw_text_with_outline('RESTART', large_font, (157,57,25), 'black', 0, (c.SCREEN_WIDTH + c.SIDE_PANEL) / 2 , 425, center= True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #print(pygame.mouse.get_pos())
            if 0 < mouse_pos[0] < c.SCREEN_WIDTH and 0 < mouse_pos[1] < c.SCREEN_HEIGHT:
                turret = select_turret() # turret = None if can't select 
                if selected_turret:
                    if not current_info_panel_rect.collidepoint(mouse_pos):
                        selected_turret = None
                        clear_selection()
                        current_info_panel_rect = pygame.Rect(0, 0, 0, 0)
                        if turret:
                            selected_turret = turret
                            selected_turret.selected = True
                elif placing_turrets:
                    if can_place:
                        create_turret()
                elif turret:
                    selected_turret = turret
                    selected_turret.selected = True
        if game_state == 'playing' or game_state == 'setting':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state == 'setting':
                    game_state = 'playing'
                else:
                    game_state = 'setting'
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                music = not music
                set_music_volume(1 if music else 0)

    if show_fps:
        if pygame.time.get_ticks() - last_update_fps > delay_update_fps_time:
            current_fps = min(max_fps, round(clock.get_fps()))
            draw_text_with_outline('FPS: ' + str(current_fps), large_font, 'white', 'black', 0, 30 , 725, center= False)
            last_update_fps = pygame.time.get_ticks()
            last_fps = current_fps
        else:
            draw_text_with_outline('FPS: ' + str(last_fps), large_font, 'white', 'black', 0, 30 , 725, center= False)

    pygame.display.update()

pygame.quit()
quit()