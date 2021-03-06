import arcade
import sys
from models import Ship,World,Background,ShipBullet,Alien



SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
SCREEN_TITLE = "MR. ROCKET"

routes = {
    'menu' : 0,
    'howtoplay' : 1,
    'game' : 2,
    'exit' :3,
}

choices = { 
    0 : 'game',
    1 : 'menu',
    2 : 'exit'
}

menu_choices = { 
    0 : 'game',
    1 : 'howtoplay',
    2 : 'exit'
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
        self.bullet = arcade.Sprite('./images/bullet.png', scale = 0.25)
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
                self.alien = arcade.Sprite('./images/alien1.png', scale = 0.5)
                self.draw_sprite(self.alien, a.x, a.y)
            if a.index[0] == 1:
                self.alien = arcade.Sprite('./images/alien2.png', scale = 0.4)
                self.draw_sprite(self.alien, a.x, a.y)
            if a.index[0] == 2:
                self.alien = arcade.Sprite('./images/alien3.png', scale = 0.5)
                self.draw_sprite(self.alien, a.x, a.y)
    
class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.current_route = routes['menu']
        self.selecting_choice = 0
        self.menu_setup()
        self.game_over_setup()
        self.set_mouse_visible(False)
        self.game_setup(width, height)
        self.game_cover = arcade.load_texture('images/background1.png')
        self.how_to_play = arcade.load_texture('images/gameguide.png')
        self.gameover = arcade.load_texture('images/bluebg.png')


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


        self.start.center_x, self.start.center_y = self.width//2, self.height//2 - 150
        self.how_to_play.center_x, self.how_to_play.center_y = self.width//2, self.height//2 - 250
        self.start.select()
        self.how_to_play.unselect()

        self.choice_list.append(self.start)
        self.choice_list.append(self.how_to_play)
    
    def game_over_setup(self):

        self.game_over_choice_list = arcade.SpriteList()

        # restartbutton
        self.restart = MenuChoiceSprite()
        self.restart.textures.append(arcade.load_texture("images/RESTART.png"))
        self.restart.textures.append(arcade.load_texture("images/RESTARTPRESS.png"))
        self.restart.set_texture(0)
        self.restart.texture_change_frames = 10

        # menubutton
        self.menu = MenuChoiceSprite()
        self.menu.textures.append(arcade.load_texture("images/MENU.png"))
        self.menu.textures.append(arcade.load_texture("images/MENUPRESS.png"))
        self.menu.set_texture(0)
        self.menu.texture_change_frames = 10

        # exitbutton
        self.exit = MenuChoiceSprite()
        self.exit.textures.append(arcade.load_texture("images/EXIT.png"))
        self.exit.textures.append(arcade.load_texture("images/EXITPRESS.png"))
        self.exit.set_texture(0)
        self.exit.texture_change_frames = 10

        self.restart.center_x, self.restart.center_y = self.width//2, self.height//2 - 100
        self.menu.center_x, self.menu.center_y = self.width//2, self.height//2 - 200
        self.exit.center_x, self.exit.center_y = self.width//2, self.height//2 - 300
        
        self.start.select()
        self.menu.unselect()
        self.exit.unselect()

        self.game_over_choice_list.append(self.restart)
        self.game_over_choice_list.append(self.menu)
        self.game_over_choice_list.append(self.exit)

    
    def game_setup(self, width, height):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_sprite = ModelSprite('./images/background1.png', model=self.world.background)
        self.background_sprite_2 = ModelSprite('./images/background2.png', model=self.world.background2)
        self.ship_sprite = ModelSprite('./images/ship.png',model=self.world.ship, scale = 0.35)
        self.bullet = BulletSprite(self.world.bullet_list)
        self.alien = AlienSprite(self.world.alien_list)


    def draw_heart(self):
        for i in self.world.heart_list:
            ModelSprite('./images/fullheart.png',model=i, scale = 0.2).draw()
    
    def draw_heart_bar(self):
        pic1 = ['images/fullheart.png', 'images/fullheart.png', 'images/fullheart.png']
        pic2 = ['images/fullheart.png', 'images/fullheart.png', 'images/emptyheart.png']
        pic3 = ['images/fullheart.png', 'images/emptyheart.png', 'images/emptyheart.png']

        count = 0
        for i in range(900, 1050, 70):
            if not self.world.ship.is_dead:
                if self.world.ship.hp_ship == 2:
                    a = arcade.Sprite(pic2[count], scale = 0.25)
                elif self.world.ship.hp_ship == 3:
                    a = arcade.Sprite(pic1[count], scale = 0.25)
                else:
                    a = arcade.Sprite(pic3[count], scale = 0.25)
                a.center_x = i
                a.center_y = SCREEN_HEIGHT - 50
                a.draw()
                count += 1

    def draw_menu(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_cover)
        self.choice_list.draw()
    
    def draw_game_running(self):
        self.background_sprite.draw()
        self.background_sprite_2.draw()
        self.ship_sprite.draw()
        self.bullet.draw()
        self.alien.draw()
        self.draw_heart_bar()
        self.draw_heart()
         # draw score
        arcade.draw_text("Score : " + str(self.world.score), SCREEN_WIDTH - 180, SCREEN_HEIGHT - 125, arcade.color.WHITE, 20)

    def draw_how_to_play(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.how_to_play)

    def hightest_score(self):
        file = open("highestscore.txt").readline()
        if file == "" or int(file) < int(self.world.lastest_score):
            with open("highestscore.txt", "w") as file:
                file.write(str(self.world.lastest_score))
        with open("highestscore.txt", "r") as file:
            score = file.readline()
        return score

    def draw_game_over(self):
        if self.world.ship.hp_ship == 0:
            score = self.hightest_score()
            self.world.die()
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.gameover)
            game_over = arcade.Sprite('images/game_over_text.png', center_x = SCREEN_WIDTH // 2, center_y = SCREEN_HEIGHT - 150, scale = 0.25)
            game_over.draw()
            arcade.draw_text(str(self.world.lastest_score), SCREEN_WIDTH // 2, 400, arcade.color.BLACK, 60)
            # hightest_score
            arcade.draw_text("HIGHEST SCORE : " + str(score), 420, 330, arcade.color.BLACK, 20)
            self.game_over_choice_list.draw()

    
    def on_draw(self):
        arcade.start_render()
        if self.current_route == routes['menu']:
            self.draw_menu()
            game_title = arcade.Sprite('images/textcover.png', center_x = SCREEN_WIDTH // 2, center_y = SCREEN_HEIGHT // 2, scale = 1)
            game_logo = arcade.Sprite('images/ship_upright.png', center_x = SCREEN_WIDTH // 2, center_y = SCREEN_HEIGHT - 280, scale = 0.55)
            game_title.draw()
            game_logo.draw()
        elif self.current_route == routes['howtoplay']:
            self.draw_how_to_play()
        elif self.current_route == routes['game']:
            self.draw_game_running()
            self.draw_game_over()
        elif self.current_route == routes['exit']:
            sys.exit()

    def update_selected_choice(self):
        if self.current_route == routes['menu']:
            for choice in self.choice_list:
                choice.unselect()
                choice.set_texture(0)
            self.choice_list[self.selecting_choice].select()    

        elif self.current_route == routes['game']:
            for choice in self.game_over_choice_list:
                choice.unselect()
                choice.set_texture(0)
            self.game_over_choice_list[self.selecting_choice].select()    

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
            self.draw_game_over()
            for choice in self.game_over_choice_list:
                if choice.is_select == True:
                    choice.update()
                    choice.update_animation()
        elif self.current_route == routes['exit']:
            sys.exit()
        
    def on_key_press(self, key, key_modifiers):
        if self.current_route == routes['menu']:
            if key == arcade.key.DOWN:
                if self.selecting_choice < 1:
                    self.selecting_choice += 1
                else:
                    self.selecting_choice = 0
                self.update_selected_choice()
            elif key == arcade.key.UP:
                if self.selecting_choice > 0 :  
                    self.selecting_choice -= 1
                else:
                    self.selecting_choice = 1
                self.update_selected_choice()       
            elif key == arcade.key.ENTER:
                self.current_route = routes[menu_choices[self.selecting_choice]]

        elif self.current_route == routes['howtoplay']:
            if key == arcade.key.ENTER:
                self.current_route = routes['game']
    
        elif self.current_route == routes['game']:
            self.world.ship_on_key_press(key, key_modifiers)
            if not self.world.is_dead():
                self.world.start()
            elif self.world.is_dead():
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
                    if self.current_route == routes['game']:
                        self.game_setup(SCREEN_WIDTH,SCREEN_HEIGHT)
                        self.world.start()
                    elif self.current_route == routes['menu']:
                        self.draw_menu()
                        self.game_setup(SCREEN_WIDTH,SCREEN_HEIGHT)

    def on_key_release(self, key, key_modifiers):
        if self.current_route == routes['game']:
            self.world.ship_on_key_release(key,key_modifiers)

def main():
    SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
    
if __name__ == '__main__':
    main()
