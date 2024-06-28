import pygame
import random
import copy
import sys
from env import *

class Tile:
    tile_type = int
    health = int
    def __init__(self, tile_type, health=0):
        self.tile_type = tile_type
        self.health = health


class Game:
    tile_size =int
    def __init__(self, screen_width, screen_height, tile_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size
        self.cols = self.screen_width // self.tile_size
        self.rows = self.screen_height // self.tile_size
        self.map = self.generate_map()
        self.map = self.replace_water_with_ponds()
        self.CollBoxes = self.genCollBoxes()


    def replace_water_with_ponds(self):

        map = copy.deepcopy(self.map)
        
        # for i in range(len(map)):
        #     for j in range(len(map)):
        #         print(f"{map[i][j].tile_type}", end=' ')
        #     print()
        # print ((len(map),len(map[0])))
        for i in range(1,len(map)-1):
            for j in range(1,len(map[i])-1):
                if self.map[i][j].tile_type == water:
                    pond_names = list(ponds.keys())
                    random_pond_name = random.choice(pond_names)
                    pond_matrix = ponds[random_pond_name]
                    map[i][j].tile_type=land
                    
                    for pi in range(len(pond_matrix)):
                        for pj in range(len(pond_matrix[pi])):
                            if pond_matrix[pi][pj] == 1:
                                if 0 <= i + pi < len(map) and 0 <= j + pj < len(map[i]):
                                    map[i + pi][j + pj].tile_type = water
            # print()
        
        # for i in range(len(map)):
        #     for j in range(len(map[i])):
        #         print(f"{map[i][j].tile_type}", end=' ')
        #     print()
        # print("\n\n")
        # for i in range(len(map)):
        #     for j in range(len(map[i])):
        #         print(f"{self.map[i][j].tile_type}", end=' ')
        #     print()
        return map

    def generate_map(self):
        game_map = []
        for row in range(self.rows):
            game_map.append([])
            for col in range(self.cols):
                if row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1:
                    game_map[row].append(Tile(water))
                else:
                    weights = [1,20,16,3,60]
                    tile_type = random.choices(blocks,weights)[0]
                    health = 0
                    for i in range(len(blocks)):
                        if tile_type == blocks[i]:
                            health = endurance[i]

                    game_map[row].append(Tile(tile_type, health))

        game_map[self.rows//2][self.cols//2].tile_type = land
        return game_map
    


    def genCollBoxes(self):
        boxes=[]
        for row in range(self.rows):
            for col in range(self.cols):
                tile_type = self.map[row][col].tile_type
                if tile_type in [stone,tree,diamond]:
                    tile_rect = pygame.Rect(
                        col * self.tile_size,
                        row * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    boxes.append(tile_rect)
        #print(boxes)
        return boxes

    def draw_map(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.map[row][col]
                if tile.tile_type == water:
                    sprite = water_img
                elif tile.tile_type == land:
                    sprite = land_img
                elif tile.tile_type == tree:
                    sprite = tree_img
                elif tile.tile_type == stone:
                    sprite = stone_img
                elif tile.tile_type == diamond:
                    sprite = diamond_img
                screen.blit(sprite, (col * self.tile_size, row * self.tile_size))


