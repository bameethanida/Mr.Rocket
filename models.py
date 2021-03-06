import arcade.key
from random import randint,choices

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

BACKGROUND_SPEED = 0.5
MOVEMENT_SPEED = 20

HEART_SPEED = 8

BULLET_SPEED = 20
BULLET_RANGE = 1000
BULLET_RADIUS = 32
RANGE_START = 30
BULLET_DAMAGE = 1

INDEX = [0,1,2]
SPEED_ALIEN_CHOICE = [2, 3, 5]
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
        self.speed_increase = 1
        self.speed = SPEED_ALIEN_CHOICE[self.index[0]] * (self.speed_increase * 1.5)
        self.hp_alien = HP_ALIEN_CHOICE[self.index[0]]
        self.score_alien = SCORE_ALIEN_CHOICE[self.index[0]]
        self.is_dead = False

    def move(self):
        self.x -= self.speed
    
    def generate_new_speed(self):
        if 0 <= self.world.score < 60:
            self.speed = SPEED_ALIEN_CHOICE[self.index[0]]
        elif 60 <= self.world.score < 120:
            self.speed = SPEED_ALIEN_CHOICE[self.index[0]] * 2
        elif 120 <= self.world.score < 170:
            self.speed = SPEED_ALIEN_CHOICE[self.index[0]] * 3
        elif 170 <= self.world.score < 260:
            self.speed = SPEED_ALIEN_CHOICE[self.index[0]] * 5
        else:
            self.speed = SPEED_ALIEN_CHOICE[self.index[0]] * 6
        
   
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
        self.generate_new_speed()
        self.alien_dead()
        self.remove_alien()

class Heart:
    def __init__(self, world):
        self.world = world
        self.x = self.world.width - 1
        self.y = randint(50, SCREEN_HEIGHT - 50)
        self.speed = HEART_SPEED 

    def move(self):
        self.x -= self.speed

    def remove_heart(self):
        if self.x < 0:
            self.world.heart_list.remove(self)
        
    def update(self, delta):
        self.move()
        self.remove_heart()

class ShipBullet:
    def __init__(self, world, x, y):
        self.world = world
        self.x = 165
        self.y = y
        self.direction = None
    
    def out_of_world(self):
        if self.x + BULLET_RADIUS < 0 or self.x - BULLET_RADIUS > self.world.width:
            return True
    
    def check_bullet_hit_alien(self):
        for i in self.world.alien_list:
            if abs(self.x - i.x) <= 50 and abs(self.y - i.y) <= 50:
                i.hp_alien -= BULLET_DAMAGE
                self.world.bullet_list.remove(self)

    def move(self):
        self.x += BULLET_SPEED * DIR_OFFSETS[DIR_RIGHT][0]
    
    def update(self,delta):
        self.move()
        if self.world.alien_list != []:
            self.check_bullet_hit_alien()
        if self.out_of_world():
            if self.world.bullet_list != []:
                self.world.bullet_list.remove(self)

class World:

    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3
    
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.state = World.STATE_FROZEN
        self.background = Background(self, 550, 350)
        self.background2 = Background(self, 1650, 350)
        self.ship = Ship(self, 100, 100)
        self.bullet_list = []
        self.alien_list = []
        self.heart_list = []
        self.frame = 0
        self.score = 0
        self.lastest_score = 0

    def display_score(self):
        if self.ship.hp_ship == 0:
            self.lastest_score = self.score

    def moving_background(self):
        if self.background.x == -550:
            self.background.x = 1650

        if self.background2.x == -550:
            self.background2.x = 1650
    
    def generate_alien(self):
        if self.frame % 60 == 0 and len(self.alien_list) <= 10:
            self.alien_list.append(Alien(self))

    def generate_heart(self):
        if self.frame % 600 == 0 and len(self.heart_list) <= 0:
            self.heart_list.append(Heart(self))
    
    def alien_hit_ship(self):
            for i in self.alien_list:
                if i.x <= self.ship.x + 120:
                    if self.ship.y - 50 <= i.y <= self.ship.y + 50:
                        self.ship.hp_ship -= 1
                        self.alien_list.remove(i)

    def collect_heart(self):
        for i in self.heart_list:
            if i.x <= self.ship.x + 100:
                if self.ship.y - 50 <= i.y <= self.ship.y + 50:
                    self.heart_list.remove(i)
                    if 0 < self.ship.hp_ship < 3:
                        powerup_sound = arcade.sound.load_sound("powerup.wav")
                        arcade.sound.play_sound(powerup_sound)
                        self.ship.hp_ship += 1
                        
    
    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN     

    def is_started(self):
        return self.state == World.STATE_STARTED 

    def die(self):
        self.state = World.STATE_DEAD
 
    def is_dead(self):
        return self.state == World.STATE_DEAD    

    def ship_on_key_press(self, key, key_modifiers):
        if key in KEY_MAP:
            self.ship.speed = MOVEMENT_SPEED
            self.ship.next_direction = KEY_MAP[key]
            if not self.ship.direction == self.ship.next_direction:
                self.ship.direction = self.ship.next_direction
        if key == arcade.key.SPACE:
            bullet = ShipBullet(self, self.ship.x + (RANGE_START * DIR_OFFSETS[self.ship.current_direction][0]), self.ship.y)
            shoot_sound = arcade.sound.load_sound("sound.mp3")
            arcade.sound.play_sound(shoot_sound)
            self.bullet_list.append(bullet)
    
    def ship_on_key_release(self, key, modifiers):
        if key in KEY_MAP:
            if self.ship.direction != DIR_STILL:
                self.ship.direction = DIR_STILL
                self.ship.speed = 0
            if not self.ship.direction == self.ship.next_direction:
                self.ship.direction = self.ship.next_direction

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return  
        self.generate_alien()
        self.generate_heart()
        self.background.update(delta)
        self.background2.update(delta)
        self.moving_background()
        self.ship.update(delta)
        self.alien_hit_ship()
        self.collect_heart()
        self.display_score()
        self.frame += 1
        for i in self.bullet_list:
            i.update(delta)
        for i in self.alien_list:
            i.update(delta)
        for i in self.heart_list:
            i.update(delta)