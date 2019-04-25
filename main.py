import arcade
from models import Ship,World,Background,ShipBullet,Alien


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()


class BulletSprite:
    def __init__(self,bullet_list):
        self.bullet = arcade.Sprite('./images/bullet.png')
        self.bullet_list = bullet_list
    
    def draw_sprite(self, sprite, x, y):
        sprite.set_position(x, y)
        sprite.draw()

    def draw(self):
        for bullet in self.bullet_list:
            self.draw_sprite(self.bullet, bullet.x, bullet.y)

class AlienSprite:
    def __init__(self, alien_list):
        self.alien_list = alien_list
        self.alien = arcade.Sprite('./images/alien1.png')
    

    def draw_sprite(self, sprite, x, y):
        sprite.set_position(x, y)
        sprite.draw()
    
    def draw(self):
        for a in self.alien_list:
            if a.index[0] == 0:
                self.alien = arcade.Sprite('./images/alien1.png')
                self.draw_sprite(self.alien, a.x, a.y)
            if a.index[0] == 1:
                self.alien = arcade.Sprite('./images/alien2.png')
                self.draw_sprite(self.alien, a.x, a.y)
            if a.index[0] == 2:
                self.alien = arcade.Sprite('./images/alien3.png')
                self.draw_sprite(self.alien, a.x, a.y)


class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):

        super().__init__(width, height)

        self.world = World(width, height)
        self.background_sprite = ModelSprite('./images/background.jpg', model=self.world.background)
        self.background_sprite_2 = ModelSprite('./images/background2.jpg', model=self.world.background2)
        self.ship_sprite = ModelSprite('./images/ship.png',model=self.world.ship)
        self.bullet = BulletSprite(self.world.bullet_list)
        self.alien = AlienSprite(self.world.alien_list)

    def on_draw(self):
        arcade.start_render()
        self.background_sprite.draw()
        self.background_sprite_2.draw()
        self.ship_sprite.draw()
        self.bullet.draw()
        self.alien.draw()
    
    def update(self, delta):
        self.world.update(delta)

    def on_key_press(self, key, key_modifiers):
        self.world.ship_on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.world.ship_on_key_release(key,key_modifiers)


def main():
    SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
    
if __name__ == '__main__':
    main()