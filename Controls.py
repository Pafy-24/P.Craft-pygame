import pygame
from typing import Callable, List, Tuple

class Controls:
    __functions = [int, Callable]
    __special =[pygame.key, Callable]
    __locked = False
    def __init__(self):
        self.__functions: List[Tuple[int, Callable]] = []
        self.__special: List[Tuple[int, Callable]] = []

    def lock(self):
        self.__locked = True
    def unlock(self):
        self.__locked = False

    def addControl(self, key_code, func):
        self.__functions.append((key_code, func))

    def addControl(self, Key: pygame.key, func):
        self.__special.append((Key, func))
    
    def press(self, key_code, *params) -> None:
        if(not self.__locked):
            for code, func in self.__functions:
                if code == key_code:
                    func(key_code, *params)
                    return
            for code, func in self.__special:
                if code == key_code:
                    func(key_code, *params)
                    return
    
    def getControls(self) -> List[Tuple[int, Callable]]:
        return self.__functions

    