import arcade
from models import Ship,World,Background,ShipBullet,Alien


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700

routes = {
    'menu' : 0,
    'howtoplay' : 1,
    'game' : 2,
}

choices = {
    'game' : 0,
    'howtoplay' : 1,
    'exit' : 2,
}

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

class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        self.is_select = False

        super().__init__(*args, **kwargs)

    def select(self):
        self.is_select = True

    def unselect(self):
        self.is_select = False

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

        self.current_route = routes['menu']
        self.selecting_choice = 0
        self.menu_setup()
        self.set_mouse_visible(False)
        self.game_setup(width, height)
        self.how_to_play = arcade.load_texture('images/guide.png')

    def menu_setup(self):
        self.choice_list = arcade.SpriteList()

        # startbutton
        self.start = MenuChoiceSprite()
        self.start.textures.append(arcade.load_texture("images/START.png"))
        self.start.textures.append(arcade.load_texture("images/STARTPRESS.png"))
        self.start.set_texture(0)
        self.start.texture_change_frames = 10

        # how_to_playbutton
        self.how_to_play = MenuChoiceSprite()
        self.how_to_play.textures.append(arcade.load_texture("images/HOWTOPLAY.png"))
        self.how_to_play.textures.append(arcade.load_texture("images/HOWTOPLAY PRESS.png"))
        self.how_to_play.set_texture(0)
        self.how_to_play.texture_change_frames = 10


        self.start.center_x, self.start.center_y = self.width//2, self.height//2 + 50
        self.how_to_play.center_x, self.how_to_play.center_y = self.width//2, self.height//2 - 20
        self.start.select()

        self.choice_list.append(self.start)
        self.choice_list.append(self.how_to_play)

    def game_setup(self, width, height):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_sprite = ModelSprite('./images/background.jpg', model=self.world.background)
        self.background_sprite_2 = ModelSprite('./images/background2.jpg', model=self.world.background2)
        self.ship_sprite = ModelSprite('./images/ship.png',model=self.world.ship)
        self.bullet = BulletSprite(self.world.bullet_list)
        self.alien = AlienSprite(self.world.alien_list)


    def draw_star(self):
        for i in self.world.star_list:
            ModelSprite('./images/fullstar.png',model=i, scale = 0.019).draw()
    
    def draw_star_bar(self):
        pic1 = ['images/fullstar.png', 'images/fullstar.png', 'images/fullstar.png']
        pic2 = ['images/fullstar.png', 'images/fullstar.png', 'images/emptystar.png']
        pic3 = ['images/fullstar.png', 'images/emptystar.png', 'images/emptystar.png']

        count = 0
        for i in range(900, 1050, 70):
            if not self.world.ship.is_dead:
                if self.world.ship.hp_ship == 2:
                    a = arcade.Sprite(pic2[count], scale = 0.03)
                elif self.world.ship.hp_ship == 3:
                    a = arcade.Sprite(pic1[count], scale = 0.03)
                else:
                    a = arcade.Sprite(pic3[count], scale = 0.03)
                a.center_x = i
                a.center_y = SCREEN_HEIGHT - 50
                a.draw()
                count += 1

    def draw_menu(self):
        self.choice_list.draw()
    
    def draw_game_running(self):
        self.background_sprite.draw()
        self.background_sprite_2.draw()
        self.ship_sprite.draw()
        self.bullet.draw()
        self.alien.draw()
        self.draw_star_bar()
        self.draw_star()
         # draw score
        arcade.draw_text("Score : " + str(self.world.score), SCREEN_WIDTH - 180, SCREEN_HEIGHT - 125, arcade.color.BLACK, 20)

    def draw_how_to_play(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.how_to_play)

    def draw_game_over(self):

        pass

    def check_state(self):
        pass
        # if self.world.state == World.STATE_DEAD:
        #     self.draw_game_over()       
    
    def on_draw(self):
        arcade.start_render()

        if self.current_route == routes['menu']:
            self.draw_menu()
        elif self.current_route == routes['howtoplay']:
            self.draw_how_to_play()
        elif self.current_route == routes['game']:
            self.draw_game_running()
        elif self.current_route == routes['exit']:
            sys.exit()

    def update_selected_choice(self):
        for choice in self.choice_list:
            choice.unselect()
            choice.set_texture(1)
        self.choice_list[self.selecting_choice].select()    

    def update(self, delta):
        if self.current_route == routes['menu']:
            for choice in self.choice_list:
                if choice.is_select == True:
                    choice.update()
                    choice.update_animation()
        elif self.current_route == routes['howtoplay']:
            pass
        elif self.current_route == routes['game']:
            self.world.update(delta)
        elif self.current_route == routes['exit']:
            sys.exit()
        
        
    def on_key_press(self, key, key_modifiers):
        self.world.ship_on_key_press(key, key_modifiers)
        if self.current_route == routes['menu']:
            if key == arcade.key.DOWN:
                if self.selecting_choice < 2:
                    self.selecting_choice += 1
                else:
                    self.selecting_choice = 0
                self.update_selected_choice()
            elif key == arcade.key.UP:
                if self.selecting_choice > 0 :  
                    self.selecting_choice -= 1
                else:
                    self.selecting_choice = 2
                self.update_selected_choice()        
            elif key == arcade.key.ENTER:
                self.current_route = routes[choices[self.selecting_choice]]

        elif self.current_route == routes['howtoplay']:
            if key == arcade.key.DELETE:
                self.current_route = routes['menu']

        elif self.current_route == routes['game']:
            self.world.ship_on_key_press(key, key_modifiers)
            
            # เขียนเงื่อนไขgameoverเพิ่ม


    def on_key_release(self, key, key_modifiers):
        if self.current_route == routes['game']:
            self.world.ship_on_key_release(key,key_modifiers)

def main():
    SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
    
if __name__ == '__main__':
    main()