import arcade
from models import Ship,World,Alien_A,Alien_B,Bullet,Background

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

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):

        super().__init__(width, height)

        self.world = World(width, height)
        self.background_sprite = ModelSprite('images/background.png', model=self.world.background)
        self.background_sprite_2 = ModelSprite('images/background2.png', model=self.world.background2)
        self.ship_sprite = ModelSprite('images/ship.png',model=self.world.ship)
        self.alien_A_sprite = ModelSprite('images/alienA.png',model=self.world.alien_A)
        self.alien_B_sprite = ModelSprite('images/alienB.png',model=self.world.alien_B)
        self.bullet = ModelSprite('images/bullet.png', model=self.world.bullet)


    def on_draw(self):

        arcade.start_render()
        self.background_sprite.draw()
        self.background_sprite_2.draw()
        self.ship_sprite.draw()
        self.alien_A_sprite.draw()
        self.alien_B_sprite.draw()
        self.bullet.draw()

    
    def update(self, delta):
        self.world.update(delta)

    def on_key_press(self, key, key_modifiers):
        self.world.bullet_on_key_press(key, key_modifiers)
        self.world.on_key_press(key, key_modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.world.on_mouse_motion(x, y, dx, dy)



def main():
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
    
if __name__ == '__main__':
    main()