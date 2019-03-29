import arcade.key
from random import randint

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750

class Ship:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
 
 
    def update(self, delta):
        pass

class Alien_A:
    def __init__(self, world, x, y, speed=0):
        self.world = world
        self.x = x
        self.y = y
        self.speed = 1

    def update(self, delta):
        if (self.x < 0):
            self.x = self.world.width - 1
            self.y = randint(50, SCREEN_HEIGHT - 50)
        self.x -= self.speed
        
class Alien_B:
    def __init__(self, world, x, y, speed=0):
        self.world = world
        self.x = x
        self.y = y
        self.speed = 3

    def update(self, delta):
        if (self.x < 0):
            self.x = self.world.width - 1
            self.y = randint(50, SCREEN_HEIGHT - 50)
        self.x -= self.speed
        
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.ship = Ship(self, 100, 100)
        self.alien_A = Alien_A(self, SCREEN_WIDTH - 1, randint(50, SCREEN_HEIGHT - 50))
        self.alien_B = Alien_B(self, SCREEN_WIDTH - 1, randint(50, SCREEN_HEIGHT - 50))

    
    def on_key_press(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        if (self.ship.y >= 50 and self.ship.y <= 700):
            self.ship.y = y
        elif (self.ship.y < 50):
            self.ship.y = 50
        elif (self.ship.y > 700):
            self.ship.y = 700
 
    def update(self, delta):
        self.ship.update(delta)
        self.alien_A.update(delta)
        self.alien_B.update(delta)
