import arcade
from models import Ship,World,Alien_A,Alien_B,Bullet

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):

        super().__init__(width, height)

        self.background = None
        self.world = World(width, height)
        self.ship_sprite = ModelSprite('images/ship.png',model=self.world.ship)
        self.alien_A_sprite = ModelSprite('images/alienA.png',model=self.world.alien_A)
        self.alien_B_sprite = ModelSprite('images/alienB.png',model=self.world.alien_B)
        self.bullet = ModelSprite('images/bullet.png', model=self.world.bullet)

    def set_up(self):

        self.background = arcade.load_texture("images/background.jpg")

    def on_draw(self):

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
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

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.set_up()
    arcade.run()