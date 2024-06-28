import pygame
import random
import sys


water, tree, stone, diamond, land = 0, 1, 2, 3, 4

ponds = {
    "pond1": [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    "pond2": [
        [0, 1, 1, 0],
        [1, 1, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 1]
    ],
    "pond3": [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 1, 1]
    ],
    "pond4": [
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 1]
    ],
    "pond5": [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0]
    ],
    "pond6": [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 1]
    ]
}

blocks =    [water, tree, stone, diamond, land]
endurance = [0, 20, 40, 75, 0]

crafting_recipes = {
    "wooden_pickaxe": [
        {'item': 'wood', 'quantity': 3}
    ],
    "stone_pickaxe": [
        {'item': 'stone', 'quantity': 2},
        {'item': 'wood', 'quantity': 1}
    ],
    "diamond_pickaxe": [
        {'item': 'diamond', 'quantity': 2},
        {'item': 'wood', 'quantity': 1}
    ],
    "wooden_axe": [
        {'item': 'wood', 'quantity': 3}
    ],
    "stone_axe": [
        {'item': 'stone', 'quantity': 3},
        {'item': 'wood', 'quantity': 1}
    ],
    "diamond_axe": [
        {'item': 'diamond', 'quantity': 3},
        {'item': 'wood', 'quantity': 1}
    ],
    "wooden_sword": [
        {'item': 'wood', 'quantity': 2}
    ],
    "stone_sword": [
        {'item': 'stone', 'quantity': 1},
        {'item': 'wood', 'quantity': 1}
    ],
    "diamond_sword": [
        {'item': 'diamond', 'quantity': 1},
        {'item': 'wood', 'quantity': 1}
    ],
    "banana_pie": [
        {'item': 'banana', 'quantity': 5}
    ],
    "banana_sword": [
        {'item': 'banana', 'quantity': 5},
        {'item': 'diamond', 'quantity': 3},
        {'item': 'wood', 'quantity': 2}
    ]
}

icons = {
    "wooden_pickaxe": None,# pygame.image.load('./Textures/wooden_pickaxe_icon.png'),
    "stone_pickaxe": None,# pygame.image.load('./Textures/stone_pickaxe_icon.png'),
    "diamond_pickaxe": None,# pygame.image.load('./Textures/diamond_pickaxe_icon.png'),
    "wooden_axe": pygame.image.load('./Textures/wooden_axe.png'),
    "stone_axe": None,# pygame.image.load('./Textures/stone_axe_icon.png'),
    "diamond_axe": None,# pygame.image.load('./Textures/diamond_axe_icon.png'),
    "wooden_sword": pygame.image.load('./Textures/wooden_sword.png'),
    "stone_sword":pygame.image.load('./Textures/stone_sword.png'),
    "diamond_sword": pygame.image.load('./Textures/diamond_sword.png'),
    "banana_pie": None,# pygame.image.load('./Textures/banana_pie_icon.png'),
    "banana_sword": pygame.image.load('./Textures/banana_sword.png'),
}


background = pygame.image.load('./Textures/background.jpg')

heart_img =  pygame.image.load('./Textures/heart.png')
lightningBolt_img =  pygame.image.load('./Textures/lightning bolt.png')
gorilla_face = pygame.image.load('./Textures/gorilla_face.png')

noimg = pygame.image.load('./Textures/64x64 Tiles/Dirty_Mossy_Tiles_64x64.png')

banana_img = pygame.image.load('./Textures/banana.png')
water_img = pygame.image.load('./Textures/64x64 Tiles/water2_64x64.png')
tree_img = pygame.image.load('./Textures/64x64 Tiles/tree_64x64.png')
stone_img = pygame.image.load('./Textures/64x64 Tiles/stone_64x64.png')
diamond_img = pygame.image.load('./Textures/64x64 Tiles/diamond_64x64.png')
land_img = pygame.image.load('./Textures/64x64 Tiles/land2_64x64.png')
player_img = pygame.image.load('./Textures/64x64 Tiles/player_64x64.png')
enemy_img = pygame.image.load('./Textures/monkey_64x64.png')
gorilla_img = pygame.image.load('./Textures/gorilla.png')
hit1_img = pygame.image.load('./Textures/64x64 Tiles/hit1_64x64.png')
hit2_img = pygame.image.load('./Textures/64x64 Tiles/hit2_64x64.png')

hit_imgs =[hit1_img, hit2_img]

def get_resource_name(resource):
    if(resource==tree):return "wood"
    if(resource==stone):return "stone"
    if(resource==diamond):return "diamond"
    if(resource==water):return "water"
    if(resource==land):return "dirt"

def get_item_icon(item):
    if(item=="stone"):return pygame.image.load('./Textures/rock.png')
    if(item=="wood"):return pygame.image.load('./Textures/tree_log.png')
    if(item=="diamond"):return pygame.image.load('./Textures/diamond.png')
    if(item=="stone"):return pygame.image.load('./Textures/rock.png')
    if(item=="stone"):return pygame.image.load('./Textures/rock.png')

black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
gray = (128, 128, 128)
maroon = (128, 0, 0)
olive = (128, 128, 0)
purple = (128, 0, 128)
teal = (0, 128, 128)
navy = (0, 0, 128)
silver = (192, 192, 192)
lime = (0, 255, 0)
aqua = (0, 255, 255)
fuchsia = (255, 0, 255)
orange = (255, 165, 0)
brown = (165, 42, 42)
gold = (255, 215, 0)
pink = (255, 192, 203)
lightblue = (173, 216, 230)
lightgreen = (144, 238, 144)
darkblue = (0, 0, 139)
darkgreen = (0, 100, 0)
darkgray = (75, 75, 75)
darkred = (139, 0, 0)
violet = (238, 130, 238)
indigo = (75, 0, 130)
beige = (245, 245, 220)
salmon = (250, 128, 114)
khaki = (240, 230, 140)
coral = (255, 127, 80)
turquoise = (64, 224, 208)
tan = (210, 180, 140)
lavender = (230, 230, 250)
orchid = (218, 112, 214)
sienna = (160, 82, 45)
plum = (221, 160, 221)
crimson = (220, 20, 60)




def line_intersect_line(p1, p2, p3, p4):
    """ Check if line segment p1-p2 intersects with line segment p3-p4 """
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def line_rect_collision(start, end, rect):
    rect_left = rect.x
    rect_right = rect.x + rect.width
    rect_top = rect.y
    rect_bottom = rect.y + rect.height

    # Define rectangle corners
    top_left = (rect_left, rect_top)
    top_right = (rect_right, rect_top)
    bottom_left = (rect_left, rect_bottom)
    bottom_right = (rect_right, rect_bottom)

    # Check if the line intersects any of the rectangle's edges
    if (line_intersect_line(start, end, top_left, top_right) or
        line_intersect_line(start, end, top_left, bottom_left) or
        line_intersect_line(start, end, bottom_left, bottom_right) or
        line_intersect_line(start, end, top_right, bottom_right)):
        return True

    # Additionally, check if one of the endpoints is inside the rectangle
    if (rect_left <= start[0] <= rect_right and rect_top <= start[1] <= rect_bottom):
        return True
    if (rect_left <= end[0] <= rect_right and rect_top <= end[1] <= rect_bottom):
        return True

    return False

def get_bounding_box(x, y, size):
    rect = pygame.Rect(
        x - size // 2,
        y - size // 2,
        size,
        size
    )
    return rect

def check_collision(x, y, size, game):
    player_rect = get_bounding_box(x, y, size)
    
    rows = len(game.map)
    cols = len(game.map[0]) if rows > 0 else 0
    
    for box in game.CollBoxes:
        if player_rect.colliderect(box):
            return True
    return False