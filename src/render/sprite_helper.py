import pygame

def load_spritesheet():
    return pygame.image.load("assets/spritesheet.png").convert_alpha()
    
def cut_sprite(sheet, rect):
    sprite = sheet.subsurface(rect)
    return sprite

def get_bird_sprite(scale_ratio):
    sheet = load_spritesheet()
    bird_sprite = cut_sprite(sheet, pygame.Rect(3, 491, 17, 13))
    bird_sprite = pygame.transform.scale_by(bird_sprite, scale_ratio)
    return bird_sprite

def get_pipe_sprites(scale_ratio):
    sheet = load_spritesheet()
    pipe_bottom_sprite = cut_sprite(sheet, pygame.Rect(84, 323, 26, 160))
    pipe_bottom_sprite = pygame.transform.scale_by(pipe_bottom_sprite, scale_ratio)
    pipe_top_sprite = cut_sprite(sheet, pygame.Rect(56, 323, 26, 160))
    pipe_top_sprite = pygame.transform.scale_by(pipe_top_sprite, scale_ratio)
    return pipe_top_sprite, pipe_bottom_sprite

def get_grass_sprite(scale_ratio):
    sheet = load_spritesheet()
    grass_sprite = cut_sprite(sheet, pygame.Rect(292, 0, 459 - 292, 30))
    grass_sprite = pygame.transform.scale_by(grass_sprite, scale_ratio)
    return grass_sprite

def get_background_sprite(scale_ratio):
    sheet = load_spritesheet()
    background_sprite = cut_sprite(sheet, pygame.Rect(0, 40, 143, 195))
    background_sprite = pygame.transform.scale_by(background_sprite, scale_ratio)
    return background_sprite

def rotate_sprite(sprite, angle, center):
    rotated_sprite = pygame.transform.rotate(sprite, angle)
    rect = rotated_sprite.get_rect(center=center)
    return rotated_sprite, rect