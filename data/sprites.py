import pygame
from PIL import Image

pygame.font.init()

FONT = pygame.font.SysFont('Comic Sans MS', 32)
IMAGE_NORMAL = pygame.Surface((100, 32), pygame.SRCALPHA)
# IMAGE_NORMAL.fill((32, 22, 15))
IMAGE_HOVER = pygame.Surface((100, 32), pygame.SRCALPHA)
# IMAGE_HOVER.fill((52, 42, 35))
IMAGE_DOWN = pygame.Surface((100, 32), pygame.SRCALPHA)
# IMAGE_DOWN.fill((82, 72, 65))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, width=800, height=600):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class MiniMap(pygame.sprite.Sprite):
    def __init__(self, image, location, group, width=800, height=600):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Bars(pygame.sprite.Sprite):
    def __init__(self, color, location, width=800, height=600):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 100))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=FONT, image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_NORMAL, text='', text_color=(255, 255, 255), image='images/TextBTN_Medium', arg=''):
        super().__init__()
        self.arg = arg
        if image == '':
            self.image_normal = pygame.transform.scale(image_normal, (width, height))
            self.image_hover = pygame.transform.scale(image_hover, (width, height))
            self.image_down = pygame.transform.scale(image_down, (width, height))
        else:
            self.image_normal = pygame.image.load(image+'.png')
            self.image_normal = pygame.transform.scale(self.image_normal, (width, height))
            self.image_hover = pygame.image.load(image+'.png')
            self.image_hover = pygame.transform.scale(self.image_hover, (width, height))
            self.image_down = pygame.image.load(image+'_Pressed.png')
            self.image_down = pygame.transform.scale(self.image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        if image != '':
            text_rect = text_surf.get_rect(center=(self.image_center[0], self.image_center[1]-5))
            self.image_normal.blit(text_surf, text_rect)
            self.image_hover.blit(text_surf, text_rect)
            text_rect = text_surf.get_rect(center=(self.image_center[0], self.image_center[1]+5))
            self.image_down.blit(text_surf, text_rect)
        else:
            text_rect = text_surf.get_rect(center=self.image_center)

            for image in (self.image_normal, self.image_hover, self.image_down):
                image.blit(text_surf, text_rect)

        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                if self.arg == '':
                    self.callback()  # Call the function.
                else:
                    self.callback(self.arg)
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal


class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color=(255, 255, 255), font=FONT, align='center'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.image_center = self.image.get_rect().center
        self.text_surface = font.render(text, True, color)
        if align == 'center':
            self.text_rect = self.text_surface.get_rect(center=self.image_center)
        else:
            self.text_rect = self.text_surface.get_rect(topleft=self.image_center)
        self.image.blit(self.text_surface, self.text_rect)


class InputText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, width, height, callback, color=(255, 255, 255), font=FONT):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.callback = callback
        self.active = False
        self.font = font
        self.text = text
        self.color = color
        self.width = width
        self.height = height
        self.image_link = pygame.image.load('images/board.png')
        self.image = pygame.transform.scale(self.image_link, (self.width, self.height))
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(topleft=(self.image.get_rect().topleft[0] + 15,
                                                             self.image.get_rect().topleft[1] + 2))
        self.image.blit(self.text_surface, self.text_rect)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def create(self):
        self.image = pygame.transform.scale(self.image_link, (self.width, self.height))
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(topleft=(self.image.get_rect().topleft[0]+15,
                                                             self.image.get_rect().topleft[1]+2))
        self.image.blit(self.text_surface, self.text_rect)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.create()
            if not self.rect.collidepoint(event.pos) and self.active is True:
                self.active = False
                self.create()
                self.callback(self.text)
        if event.type == pygame.KEYDOWN and self.active is True:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.create()
            elif event.key == pygame.K_RETURN:
                self.active = False
                self.create()
                self.callback(self.text)
            elif len(self.text) < 6:
                self.text += event.unicode
                self.create()


def get_map_image():
    im = Image.open(r'images\minimap.png')
    w, h = im.size
    i = 0
    images = []
    while i+7 < w:
        im1 = im.crop((i, 0, i+7, h))
        i += 7
        mode = im1.mode
        size = im1.size
        data = im1.tobytes()

        py_image = pygame.image.fromstring(data, size, mode)
        images.append(py_image)

    return images
