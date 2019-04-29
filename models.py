import arcade.key
from random import randint,choices

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

BACKGROUND_SPEED = 1
MOVEMENT_SPEED = 10

STAR_SPEED = 8

BULLET_SPEED = 15
BULLET_RANGE = 1000
BULLET_RADIUS = 32
RANGE_START = 30
BULLET_DAMAGE = 1

INDEX = [0,1,2]
SPEED_ALIEN_CHOICE = [randint(2,3), randint(4,5), 6]
HP_ALIEN_CHOICE = [1, 3, 5]
SCORE_ALIEN_CHOICE = [5, 10, 20]


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
        self.hp_ship = 3
        self.is_dead = False
    
    def ship_dead(self):
        if self.hp_ship <= 0:
            self.is_dead = True


    def set_current_direction(self):
        if not self.direction == DIR_STILL:
            self.current_direction = self.direction
    
    def move(self):
        if self.y > 650:
            self.y = 650
            self.direction = DIR_STILL
        elif self.y < 50:
            self.y = 50
            self.direction = DIR_STILL
        else:
            self.y += self.speed * DIR_OFFSETS[self.direction][1]

    def update(self, delta):
        self.move()
        self.ship_dead()

class Alien:
    def __init__(self, world):
        self.world = world
        self.x = self.world.width - 1
        self.y = randint(50, SCREEN_HEIGHT - 50)
        self.index = choices(INDEX, weights = [4, 2, 1])
        self.speed = SPEED_ALIEN_CHOICE[self.index[0]]
        self.hp_alien = HP_ALIEN_CHOICE[self.index[0]]
        self.score_alien = SCORE_ALIEN_CHOICE[self.index[0]]
        self.is_dead = False

    def move(self):
        self.x -= self.speed
    
    def alien_dead(self):
        if self.hp_alien <= 0:
            self.is_dead = True
    
    def remove_alien(self):
        if self.x < 0:
            self.world.alien_list.remove(self) 
        if self.is_dead == True:
            self.world.score += self.score_alien
            self.world.alien_list.remove(self)
        
    def update(self, delta):
        self.move()
        self.alien_dead()
        self.remove_alien()

class Star:
    def __init__(self, world):
        self.world = world
        self.x = self.world.width - 1
        self.y = randint(50, SCREEN_HEIGHT - 50)
        self.speed = STAR_SPEED 

    def move(self):
        self.x -= self.speed

    def remove_star(self):
        if self.x < 0:
            self.world.star_list.remove(self)
        
    def update(self, delta):
        self.move()
        self.remove_star()

class ShipBullet:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = None
    
    def out_of_world(self):
        if self.x + BULLET_RADIUS < 0 or self.x - BULLET_RADIUS > self.world.width:
            return True
    
    def check_bullet_hit_alien(self):
        for i in self.world.alien_list:
            if abs(self.x - i.x) <= 20 and abs(self.y - i.y) <= 20:
                i.hp_alien -= BULLET_DAMAGE
                self.world.bullet_list.remove(self)

    def move(self):
        self.x += BULLET_SPEED * DIR_OFFSETS[DIR_RIGHT][0]
    
    def update(self,delta):
        self.move()
        self.check_bullet_hit_alien()
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
        self.star_list = []
        self.frame = 0
        self.score = 0
        self.game_over = False


    def moving_background(self):
        if self.background.x == -700:
            self.background.x = 2100

        if self.background2.x == -700:
            self.background2.x = 2100
    
    def generate_alien(self):
        if self.frame % 60 == 0 and len(self.alien_list) <= 10:
            self.alien_list.append(Alien(self))

    def generate_star(self):
        if self.frame % 600 == 0 and len(self.star_list) <= 0:
            self.star_list.append(Star(self))
    
    def alien_hit_ship(self):
        for i in self.alien_list:
            if self.ship.x + 50 <= i.x <= self.ship.x + 100:
                if self.ship.y - 50 <= i.y <= self.ship.y + 50:
                    self.ship.hp_ship -= 1
                    self.alien_list.remove(i)
    
    def collect_star(self):
        for i in self.star_list:
            if self.ship.x + 50 <= i.x <= self.ship.x + 100:
                if self.ship.y - 50 <= i.y <= self.ship.y + 50:
                    self.star_list.remove(i)
                    if 0 < self.ship.hp_ship < 3:
                        self.ship.hp_ship += 1
    
    def set_up_new_game(self) :
        self.score = 0
        self.ship.hp_ship = 3

    def game_over(self):
        if self.ship.hp_ship == 0:
            self.game_over == True
            World.set_up_new_game(self)

    def ship_on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.speed = MOVEMENT_SPEED
            self.ship.next_direction = KEY_MAP[key]
            if not self.ship.direction == self.ship.next_direction:
                self.ship.direction = self.ship.next_direction
        if key == arcade.key.SPACE:
            bullet = ShipBullet(self, self.ship.x + (RANGE_START * DIR_OFFSETS[self.ship.current_direction][0]), self.ship.y)
            self.bullet_list.append(bullet)
    
    def ship_on_key_release(self, key, modifiers):
        if key in KEY_MAP:
            if self.ship.direction != DIR_STILL:
                self.ship.direction = DIR_STILL
                self.ship.speed = 0
            
            if not self.ship.direction == self.ship.next_direction:
                self.ship.direction = self.ship.next_direction

    def update(self, delta):
        self.generate_alien()
        self.generate_star()
        self.background.update(delta)
        self.background2.update(delta)
        self.moving_background()
        self.ship.update(delta)
        self.alien_hit_ship()
        self.collect_star()
        self.game_over()
        self.frame += 1

        for i in self.bullet_list:
            i.update(delta)
        for i in self.alien_list:
            i.update(delta)
        for i in self.star_list:
            i.update(delta)