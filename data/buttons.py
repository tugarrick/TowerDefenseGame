import pygame

class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, suf):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:       
                action = True
                if self.single_click:
                    self.clicked = True

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
        
        suf.blit(self.image, self.rect)
        
        return action
    # def set_alpha(self, alpha):
    #     self.image.set_alpha(alpha)

