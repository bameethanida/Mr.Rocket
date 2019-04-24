import arcade.key
from random import randint,random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750

BACKGROUND_SPEED = 1
MOVEMENT_SPEED = 6


BULLET_SPEED = 15
BULLET_RANGE = 1000
BULLET_RADIUS = 32
RANGE_START = 30


DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_UP: (0, 1),
               DIR_RIGHT: (1, 0),
               DIR_DOWN: (0, -1),
               DIR_LEFT: (-1, 0)}

KEY_MAP = {arcade.key.UP: DIR_UP,
           arcade.key.DOWN: DIR_DOWN,
           arcade.key.LEFT: DIR_LEFT,
           arcade.key.RIGHT: DIR_RIGHT, }

SPEED_ALIEN_CHOICE = [randint(2,4), randint(5,7), 10]

class Background:
    def __init__(self, world, x,y):
        self.world = world
        self.x = x
        self.y = y

    def update(self, delta):
        self.x -= BACKGROUND_SPEED
    

class Ship:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL
        self.speed = MOVEMENT_SPEED
        self.current_direction = DIR_UP
    
    def set_current_direction(self):
        if not self.direction == DIR_STILL:
            self.current_direction = self.direction
    
    def move(self):
        if self.y > 700:
            self.y = 700
            self.direction = DIR_STILL
        elif self.y < 50:
            self.y = 50
            self.direction = DIR_STILL
        else:
            self.y += self.speed * DIR_OFFSETS[self.direction][1]

    def update(self, delta):
        self.move()


class Alien:
    def __init__(self, world, hp_alien):
        self.world = world
        self.x = self.world.width - 1
        self.y = randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.choices(SPEED_ALIEN_CHOICE, weight = [60, 30, 10])
        self.hp_alien = hp_alien

    def random_height(self):
        if (self.x < 0):
            self.x = self.world.width - 1
            self.y = randint(50, SCREEN_HEIGHT - 50)

    def move(self):
        self.x -= self.speed

    def update(self, delta):
        self.random_height()
        self.move()


class Bullet:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = None
    
    def out_of_world(self):
        if self.x + BULLET_RADIUS < 0 or self.x - BULLET_RADIUS > self.world.width:
            return True


class ShipBullet(Bullet):
    def __init__(self,world,x,y):
        super().__init__(world,x,y)
    
    def move(self):
        self.x += BULLET_SPEED * DIR_OFFSETS[DIR_RIGHT][0]
    
    def update(self,delta):
        self.move()
        if self.out_of_world():
            if self.world.bullet_list != []:
                self.world.bullet_list.remove(self)



class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = Background(self,700,375)
        self.background2 = Background(self,2100,375)
        self.ship = Ship(self, 100, 100)
        self.bullet_list = []
        self.alien_list = []


    def moving_background(self):
        if self.background.x == -700:
            self.background.x = 2100

        if self.background2.x == -700:
            self.background2.x = 2100
    
    def generate_alien(self):
        pass

    def ship_on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.speed = MOVEMENT_SPEED
            self.ship.next_direction = KEY_MAP[key]
            if not self.ship.direction == self.ship.next_direction:
                self.ship.direction = self.ship.next_direction
        if key == arcade.key.SPACE:
            bullet = ShipBullet(self, self.ship.x + (RANGE_START * DIR_OFFSETS[self.ship.current_direction][0]),
                self.ship.y)
            self.bullet_list.append(bullet)
    
    def ship_on_key_release(self, key, modifiers):
        if key in KEY_MAP:
            if self.ship.direction != DIR_STILL:
                self.ship.direction = DIR_STILL
                self.ship.speed = 0
            
            if not self.ship.direction == self.ship.next_direction:
                self.ship.direction = self.ship.next_direction


    def update(self, delta):
        self.background.update(delta)
        self.background2.update(delta)
        self.moving_background()
        self.ship.update(delta)
        for i in self.bullet_list:
            i.update(delta)
        for i in self.alien_list:
            i.update(delta)