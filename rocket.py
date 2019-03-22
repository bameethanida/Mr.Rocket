import arcade
from models import Ship,World,Meteorite
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750
 
class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)
 
        self.world = World(width, height)
        self.ship_sprite = ModelSprite('images/dot.png',model=self.world.ship)
        self.meteorite_sprite = ModelSprite('images/dot.png',model=self.world.meteorite)
        
 
 
    def on_draw(self):
        arcade.start_render()
        self.ship_sprite.draw()
        self.meteorite_sprite.draw()
 
    def update(self, delta):
        self.world.update(delta)

    def on_key_press(self, key, key_modifiers):
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
    arcade.run()
