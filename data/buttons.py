import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font, image_normal, image_hover,
                 image_down, text='', text_color=(0, 0, 0)):
        super().__init__()
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
        self.image_down = pygame.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
                self.callback()


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, width, height, font):
        pygame.sprite.Sprite.__init__(self)
        self.text_surface = font.render(text, True, color)
        self.image = pygame.Surface((len(text)*17, 30))
        self.text_rect = self.text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.text_surface, self.text_rect)
        self.rect = self.image.get_rect(center=(width, height))


class InputText(pygame.sprite.Sprite):
    def __init__(self, text, color, width, height, callback, font):
        pygame.sprite.Sprite.__init__(self)
        self.callback = callback
        self.active = False
        self.font = font
        self.text = text
        self.color = color
        self.width = width
        self.height = height
        self.background_color = (30, 30, 30)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.image = pygame.Surface((200, 50))
        self.image.fill(self.background_color)
        self.text_rect = self.text_surface.get_rect(topleft=self.image.get_rect().topleft)
        self.image.blit(self.text_surface, self.text_rect)
        self.rect = self.image.get_rect(topleft=(self.width + 5, self.height))

    def create(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.image = pygame.Surface((200, 50))
        self.image.fill(self.background_color)
        self.text_rect = self.text_surface.get_rect(topleft=self.image.get_rect().topleft)
        self.image.blit(self.text_surface, self.text_rect)
        self.rect = self.image.get_rect(topleft=(self.width+5, self.height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.background_color = (50, 50, 50)
                self.create()
            if not self.rect.collidepoint(event.pos) and self.active is True:
                self.active = False
                self.background_color = (30, 30, 30)
                self.create()
                self.callback(self.text)
        if event.type == pygame.KEYDOWN and self.active is True:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
                self.background_color = (30, 30, 30)
                self.callback(self.text)
            else:
                if len(self.text) < 7:
                    self.text += event.unicode
            self.create()
