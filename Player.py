import pygame
import random
import sys
from env import *
from Controls import Controls
from Game import *
from Enemy import *
import math
from typing import Callable, List, Tuple

class Player:
    __x = int
    __y = int
    controls = None
    __speed =int
    __size = int
    __facing = [int,int]
    __attackRange = int
    __damage = int
    __forceX = int
    __forceY = int
    inventory = {}
    player_health = int 
    player_energy = int
    __locked = False
    def lock(self):
        self.__locked = True
        self.controls.lock()
    def unlock(self):
        self.__locked = False
        self.controls.unlock()

    def Move(self, button, game:Game):
        #print(f"Player BeforeMove Rectangle:{pygame.Rect(self.__x,self.__y,self.__size,self.__size)}")
            
        speed = self.__speed
        new_x = self.__x
        new_y = self.__y
        bp_x = self.__x
        bp_y = self.__y
        if button == 26: 
            new_y-= speed
            bp_y-=speed//3
           # self.__facing = [1,0]
        elif button == 4:
            new_x-=speed
            bp_x-=speed//3
           # self.__facing = [0,-1]

        elif button == 22: 
            new_y+=speed
            bp_y+=speed//3
            #self.__facing = [-1,0]
            
        elif button == 7: 
            new_x+=speed
            bp_x+=speed//3
            #self.__facing = [0,1]

        if not check_collision(new_x, new_y, self.__size, game):
            self.__x = new_x
            self.__y = new_y
        elif not check_collision(bp_x, bp_y, self.__size, game):
            self.__x = bp_x
            self.__y = bp_y
        #print(f"Player AfterMove Rectangle:{pygame.Rect(self.__x,self.__y,self.__size,self.__size)}")
        #print(self.getPos()) 

    def __init__(self, x, y, speed, size, damage=5):
        self.holding_item = None
        self.__x = x
        self.__y = y
        self.__facing=[0,-1]
        self.__size = size
        self.__speed = speed
        self.__attackRange = 50
        self.player_energy = 100
        self.player_health = 100
        self.max_health = 100
        self.__damage = damage
        self.__normal_damage = damage
        self.controls = Controls()
        self.controls.addControl(26, self.Move)
        self.controls.addControl(4, self.Move)
        self.controls.addControl(22, self.Move)
        self.controls.addControl(7, self.Move)
        self.inventory = {}
        print("PlayerInitialized")

    def collect(self,item, q=1, icon=None):
        item_name = str
        if isinstance(item,str):item_name=item
        else: item_name = get_resource_name(item)
        #print(item)
       # print(item_name)
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] += q
        else:
            if(icon == None):icon = get_item_icon(item_name)
            self.inventory[item_name] = {"icon": icon, "quantity": q}


    def can_craft(self, recipe):
        for ingredient in recipe:
            item = ingredient['item']
            required_quantity = ingredient['quantity']
            if self.inventory.get(item, {}).get('quantity', 0) < required_quantity:
                return False
        return True

    def craft(self,recipe_name):
        recipe = crafting_recipes[recipe_name]
        if not self.can_craft(recipe):
            return
        for ingredient in recipe:
            item = ingredient['item']
            required_quantity = ingredient['quantity']
            self.inventory[item]['quantity']-=required_quantity
        self.collect(recipe_name,q=1,icon = icons[recipe_name])
            

    def hit(self, screen, game:Game, enemies):
        
        if not self.__locked:
            #print("HIT")
            if(self.player_energy <10):
                return
            
            pygame.mixer.Sound('./SoundTrack/422503__nightflame__swinging-staff-whoosh-low-09.wav').play()
        
            self.player_energy-=10
            attack = {"x":int,"y":int,"size":int}
            attack["x"]=self.__x
            attack["y"]=self.__y
            attack["size"] = self.__attackRange
            #print(self.__facing)
            #print(attack)
            if self.__facing[0]==-1:
                attack['y']+=self.__attackRange
            if self.__facing[0]==1:
                attack['y']-=self.__attackRange
            if self.__facing[1]==-1:
                attack['x']-=self.__attackRange
            if self.__facing[1]==1:
                attack['x']+=self.__attackRange
            #print(attack)
            attackBox = get_bounding_box(attack["x"],attack["y"],attack["size"])
            #print(attackBox)
            
            #pygame.draw.rect(screen, red, attackSurface.get_rect())
            #print(attackSurface.get_rect())
            
            for block in game.CollBoxes:
                if attackBox.colliderect(block):
                    #print(block)
                    collected = game.map[block.y//game.tile_size][block.x//game.tile_size].tile_type
                    if collected==land:
                        print(collected)
                    game.map[block.y//game.tile_size][block.x//game.tile_size].tile_type = land
                    game.CollBoxes=game.genCollBoxes()

                    if collected == tree:
                        sound = pygame.mixer.Sound('./SoundTrack/645611__duisterwho__crunchy-snap-one-shot.wav')
                        sound.set_volume(-50)
                        sound.play()
                    
                    if collected == stone or collected==diamond:
                        pygame.mixer.Sound('./SoundTrack/661807__krokulator__low-quality-breaking-sound.wav').play()

                    self.collect(collected)
            for enemy in enemies:
                if(attackBox.colliderect(enemy.collBox())):

                    sound = pygame.mixer.Sound('./SoundTrack/335853__ipaghost__monkey5.wav')
                    sound.set_volume(50)
                    sound.play()
        
                    enemy.health-=self.__damage
                    # Push 
                    dir_x = enemy.getPos()[0] - self.__x
                    dir_y = enemy.getPos()[1] - self.__y
                    distance = (dir_x**2 + dir_y**2)**0.5
                    if distance != 0:
                        dir_x /= distance
                        dir_y /= distance
                        
                        if(enemy.gorilla==False):
                            enemy.setPos(enemy.getPos()[0] + dir_x * 25, 
                                         enemy.getPos()[1] + dir_y * 25)

            self.drawHit(screen, attackBox)
            return attackBox

    def setFacing(self, keys):
        if not self.__locked:
            #print(f"Player Facing Rectangle:{pygame.Rect(self.__x,self.__y,self.__size,self.__size)}")
            vertical =False
            horizontal = False
            anypress=False
            for key_code, pressed in enumerate(keys):
                if pressed and key_code in [4,7,22,26]:
                    anypress=True
                    if key_code==26:
                        self.__facing[0]=1
                        vertical=True
                    if key_code==4:
                        self.__facing[1]=-1
                        horizontal = True
                    if key_code==22:
                        self.__facing[0]=-1
                        vertical=True
                    if key_code==7:
                        self.__facing[1]=1
                        horizontal = True
            if(anypress==True):
                if(vertical==False):self.__facing[0]=0
                if(horizontal==False):self.__facing[1]=0

    def collBox(self):
        size = self.__size
        rect = pygame.Rect(self.__x-size//2, self.__y-size//2,size,size)
       # print(rect)
        return rect

    def draw(self, screen):
        #print(f"Player Draw Rectangle:{pygame.Rect(self.__x,self.__y,self.__size,self.__size)}")
        angle = math.degrees(math.atan2(-self.__facing[1], self.__facing[0]))
        scaled_sprite = pygame.transform.scale(player_img,(3*self.__size, 3*self.__size))
    #     scaled_sprite = player_img
        rotated_sprite = pygame.transform.rotate(scaled_sprite, angle)
        sprite_rect = rotated_sprite.get_rect(center=(self.__x, self.__y))
        screen.blit(rotated_sprite, sprite_rect.topleft)

        holding_item = self.holding_item
        if holding_item!=None and holding_item in icons and icons[holding_item]!=None:
            item_sprite = pygame.transform.scale(icons[holding_item], (self.__size,self.__size))
            item_rect = item_sprite.get_rect(center=(self.__x+20, self.__y-20))
            screen.blit(item_sprite, item_rect.topleft)


    def drawHit(self, screen, attackBox:pygame.Rect):
        
        if(attackBox == None):
            return
        size = attackBox.size[0]
        AttackCenter=attackBox.center
        angle = math.degrees(math.atan2(-self.__facing[1], self.__facing[0]))
        img = random.choice(hit_imgs)
        
        scaled_sprite = pygame.transform.scale(img,[1*size, 1*size])
        rotated_sprite = pygame.transform.rotate(scaled_sprite, angle)
        sprite_rect = rotated_sprite.get_rect(center=(AttackCenter[0], AttackCenter[1]))
        screen.blit(rotated_sprite, sprite_rect.topleft)


    def setPos(self, x, y):
        self.__x = x
        self.__y = y
    def getPos(self):
        return self.__x, self.__y
  
  
    def setSpeed(self, speed):
        self.__speed = speed
    def getSpeed(self):
        return self.__speed

    def update(self, game:Game):
        keys = pygame.key.get_pressed()
        self.setFacing(keys)
        
        for key_code, pressed in enumerate(keys):
            if pressed:
                self.controls.press(key_code, game)

        
            player_tile = [self.getPos()[0] // game.tile_size, self.getPos()[1] // game.tile_size]

            if player_tile[0] >= game.cols:
                self.setPos((game.cols) * game.tile_size, self.getPos()[1])
            if player_tile[0] < 0:
                self.setPos((0) * game.tile_size, self.getPos()[1])
            if player_tile[1] >= game.rows:
                self.setPos(self.getPos()[0], (game.rows) * game.tile_size)
            if player_tile[1] < 0:
                self.setPos(self.getPos()[0], (0) * game.tile_size)

        self.player_energy = min(self.player_energy + 1, 100)

        noMore =[]
        for item in self.inventory:
            if item==None or self.inventory[item]["quantity"]==0 :
                noMore.append(item)
        for item in noMore:
            self.inventory.pop(item)
        self.player_health = min(self.player_health, self.max_health)


        if self.holding_item==None:
            self.__damage = self.__normal_damage
        elif self.holding_item == "banana_sword":
            self.__damage = self.__normal_damage + 100
        elif self.holding_item=="wooden_sword":
            self.__damage = self.__normal_damage +5
        elif self.holding_item=="stone_sword":
            self.__damage = self.__normal_damage +10
        elif self.holding_item=="diamond_sword":
            self.__damage = self.__normal_damage +20
        else:
            self.__damage = self.__normal_damage


