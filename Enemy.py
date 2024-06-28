import pygame
import random
import sys
import math
from env import *
from Game import *
from Player import *
from DirtBall import *

class Enemy:

    def __init__(self, x, y, speed, size, Visionrange=500, damage=10, health=50, gorilla=False):
        self.health = health
        self.__max_health = health
        self.__x = x
        self.__y = y
        self.__speed = speed
        self.__vx = 0
        self.__vy = 0
        self.__max_speed = speed
        self.__last_pos_stiuta = {"x": None, "y": None}
        self.__facing = [0, 0]
        self.__size = size
        self.__range = Visionrange
        self.__damage = damage
        self.gorilla = gorilla
        self.dirt_balls = [] 
        self.throw_interval = 10000 
        self.last_throw_time = pygame.time.get_ticks() 
        print(f'Created Enemy at ({self.__x}, {self.__y}) with speed {self.__speed}')

    def throw_dirt_ball(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_throw_time >= self.throw_interval:
            dir_x = player.getPos()[0] - self.__x
            dir_y = player.getPos()[1] - self.__y
            distance = (dir_x**2 + dir_y**2)**0.5
            if distance != 0:
                dir_x /= distance
                dir_y /= distance
                dirt_ball = DirtBall(self.__x, self.__y, dir_x, dir_y)
                self.dirt_balls.append(dirt_ball)
                self.last_throw_time = current_time

    def update_dirt_balls(self, player, game, screen:pygame.Surface):
        for dirt_ball in self.dirt_balls[:]:
            dirt_ball.move()
            if dirt_ball.get_rect().colliderect(player.collBox()):
                player.player_health -= dirt_ball.damage
                self.dirt_balls.remove(dirt_ball)
            else:
                for box in game.CollBoxes:
                    if dirt_ball.get_rect().colliderect(box):
                        tile_x = box.x // game.tile_size
                        tile_y = box.y // game.tile_size
                        game.map[tile_y][tile_x].tile_type = land
                        game.CollBoxes = game.genCollBoxes()
                        break
            if dirt_ball.x>screen.get_width() or dirt_ball.x<=0:
                self.dirt_balls.remove(dirt_ball)
            
            if dirt_ball.y>screen.get_height() or dirt_ball.y<=0:
                self.dirt_balls.remove(dirt_ball)

    def draw_dirt_balls(self, screen):
        for dirt_ball in self.dirt_balls:
            dirt_ball.draw(screen)
    def follow_player(self, player, screen, game: Game):
        sees = False


        dir_x = player.getPos()[0] - self.__x
        dir_y = player.getPos()[1] - self.__y
        distance = (dir_x**2 + dir_y**2)**0.5

        if distance <= self.__range:
            # Verificam daca sunt obstacole intre player si maimuta cu un rayTracing
            #line = pygame.draw.line(screen, red, self.getPos(), player.getPos())
            sees = True
            for box in game.CollBoxes:
                if line_rect_collision(self.getPos(), player.getPos(), box):
                    sees = False
                    break

        if sees:
            self.__last_pos_stiuta["x"], self.__last_pos_stiuta["y"] = player.getPos()
            if distance != 0:
                
                dir_x /= distance
                dir_y /= distance


                self.__vx = dir_x * self.__max_speed
                self.__vy = dir_y * self.__max_speed


                self.__facing = [dir_x, dir_y]
        else:
            
            if self.__last_pos_stiuta["x"] is not None and self.__last_pos_stiuta["y"] is not None:
                dir_x = self.__last_pos_stiuta["x"] - self.__x
                dir_y = self.__last_pos_stiuta["y"] - self.__y
                distance = (dir_x**2 + dir_y**2)**0.5

                if distance != 0:
                    
                    dir_x /= distance
                    dir_y /= distance


                    self.__vx = dir_x * self.__max_speed
                    self.__vy = dir_y * self.__max_speed


                    if distance < self.__max_speed:
                        self.__vx = 0
                        self.__vy = 0
                        
                    self.__facing = [dir_x, dir_y]
                else:
                    self.__vx = 0
                    self.__vy = 0
            else:
                self.__vx = 0
                self.__vy = 0

        return sees

    def getPos(self):
        return self.__x, self.__y

    def setPos(self, x, y):
        self.__x = x
        self.__y = y

    def face2player(self, player):
        dir_x = player.getPos()[0] - self.__x
        dir_y = player.getPos()[1] - self.__y
        distance = (dir_x**2 + dir_y**2)**0.5
        dir_x /= distance
        dir_y /= distance
        self.__facing = [dir_x, dir_y]

    def drawHealthBar(self,screen:pygame.Surface): 
        screen_height = screen.get_height()
        screen_weight = screen.get_width()
        barWidth = screen_weight - 400
        icon = pygame.transform.scale(gorilla_face, (80,80))
        screen.blit(icon,(120, 60))
        fill = float(self.health / self.__max_health) * barWidth
        pygame.draw.rect(screen, black, (198, 88, barWidth+4, 34))
        pygame.draw.rect(screen, gray, (200, 90, fill, 30))

    def draw(self, screen):
        sprite = enemy_img
        if self.gorilla:sprite=gorilla_img
        #print(sprite)
        angle = math.degrees(math.atan2(-self.__facing[1], self.__facing[0])) - 90
        if self.gorilla:
            angle+=180
            self.drawHealthBar(screen)
        scaled_sprite = pygame.transform.scale(sprite, (2 * self.__size, 2 * self.__size))
        rotated_sprite = pygame.transform.rotate(scaled_sprite, angle)
        sprite_rect = rotated_sprite.get_rect(center=(self.__x, self.__y))
        #pygame.draw.rect(screen,red,sprite_rect)
        screen.blit(rotated_sprite, sprite_rect.topleft)

    def collBox(self):
        size = self.__size
        rect = pygame.Rect(self.__x - size // 2, self.__y - size // 2, size, size)
        return rect

    def touch(self, player):
        pBox = player.collBox()
        eBox = self.collBox()
        if eBox.colliderect(pBox):
            player.player_health -= self.__damage
            # Push player
            dir_x = player.getPos()[0] - self.__x
            dir_y = player.getPos()[1] - self.__y
            distance = (dir_x**2 + dir_y**2)**0.5
            if distance != 0:
                dir_x /= distance
                dir_y /= distance
                player.setPos(player.getPos()[0] + dir_x * 15, player.getPos()[1] + dir_y * 15)

    def Update(self, screen, player, game: Game):
        if self.gorilla:
            self.face2player(player)
            for box in game.CollBoxes:
                if self.collBox().colliderect(box):
                    game.map[box.y // game.tile_size][box.x // game.tile_size].tile_type = land
            game.CollBoxes = game.genCollBoxes()


        next_x = self.__x + self.__vx
        next_y = self.__y + self.__vy


        tile_x = int(next_x // game.tile_size)
        tile_y = int(next_y // game.tile_size)

        if game.map[tile_y][tile_x].tile_type != water:
            self.__x = next_x
            self.__y = next_y
        else:
            self.__vx = 0
            self.__vy = 0

        self.touch(player) 
        if self.gorilla:
            self.throw_dirt_ball(player) 
            self.update_dirt_balls(player, game, screen) 
        self.draw(screen)
        self.draw_dirt_balls(screen)  

        return self.health