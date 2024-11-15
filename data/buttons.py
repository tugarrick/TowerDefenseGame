import pygame

class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect= image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.single_click = single_click
        self.enable = True

    def set_enable(self, is_enable):
        self.enable = is_enable
    
    def draw(self, suf):

        action = False
        if self.enable:

            mouse_pos = pygame.mouse.get_pos()
            
            if self.rect.collidepoint(mouse_pos):
                print("collide")
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.clicked == False:       
                        action = True
                        if self.single_click:
                            self.clicked = True
                self.clicked = False
            # if pygame.mouse.get_pressed()[0] == False:
            #     self.clicked = False

        suf.blit(self.image, self.rect)
        # button collider debug
        pygame.draw.rect(suf, 'red', (self.rect.topleft[0], self.rect.topleft[1], self.image.get_width(), self.image.get_height()), 1)

        if action:
            print("click")

        return action
    # def set_alpha(self, alpha):
    #     self.image.set_alpha(alpha)

