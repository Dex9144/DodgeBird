import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "DodgeBird"

BIRD_SPEED = 6  # how high the bird jump
GRAVITATION = 0.4  # gravitation force

SPIKE_SPEED = 5


class Animate(arcade.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time):  # swaps between textures based on delta_time, just a preset from internet
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
                self.set_texture(self.i)


# Bird class, player controlled object, sprites from /bird/custombird
class Bird(Animate):
    def __init__(self):
        super().__init__("../Bird/CUstombird-downflap.png", 2.5)  # giving start picture and scale
        # making list for frames
        self.texture_list = [(arcade.load_texture("../Bird/CUstombird-downflap.png")),
                             (arcade.load_texture("../Bird/Custombird-midflap.png")),
                             (arcade.load_texture("../Bird/Custombird-upflap.png"))
                             ]
        # making another list for flipped frames
        self.texture_flipped_list = [
            (arcade.load_texture("../Bird/CUstombird-downflap.png", flipped_horizontally=True)),
            (arcade.load_texture("../Bird/Custombird-midflap.png", flipped_horizontally=True)),
            (arcade.load_texture("../Bird/Custombird-upflap.png", flipped_horizontally=True))
        ]

        self.time = 10  # time delay for the animation
        self.hit_sound_played = False  # player is not hitting the ground when game starts

        """Start position"""
        self.center_x = SCREEN_WIDTH / 2  # start position on x
        self.center_y = 10  # start position on y
        self.change_y = 0  # start without force

        """Start angle"""
        self.dir = ""  # direction is right
        self.angle = 0  # angle is 0
        self.change_angle = 0  # angle force is 0
        self.ANGLE_AC = 0.5

    def update(self):  # things that happen every frame
        """gravity"""
        self.center_y += self.change_y
        self.change_y -= GRAVITATION

        """Collision with screen borders"""  # makes bird stop when touching border
        if self.center_y <= 45:
            self.center_y = 45
            # Makes sound when hitting the ground
            if not self.hit_sound_played:  # If bird did not hit the ground
                arcade.play_sound((random.choice(window.hit_sound_list)))  # play the sound from \sound
                self.hit_sound_played = True  # bird did hit the ground
        # make the hit sound possible after the bird leaving the ground
        if self.center_y != 45:
            self.hit_sound_played = False

        if self.center_y >= SCREEN_HEIGHT - 20:
            self.center_y = SCREEN_HEIGHT - 20
        if self.center_x <= 26:
            self.center_x = 26
        if self.center_x >= SCREEN_WIDTH - 26:
            self.center_x = SCREEN_WIDTH - 26

        """Horizontally movement"""
        self.center_x += self.change_x  # This makes the sprite move

        """Angle"""
        self.turn_sprite()  # checking which way the bird is going
        self.angle_control()  # control the change_angle
        print(self.center_y)

    def jump(self):  # all things that happen when bird is jumping
        self.change_y = BIRD_SPEED  # bird goes up
        arcade.play_sound(window.jump_sound)  # plays the jump sound from \sound

        # the angle goes up based on what dir
        if self.dir == "right":
            self.change_angle += 50  # dip up the bird
        if self.dir == "left":
            self.change_angle += -50  # dip up the bird

    def turn_sprite(self):  # turn function manages all thing when player is turning

        if self.dir == "left":  # things that happen when bird is going left
            self.textures = self.texture_flipped_list  # using frames that are turned left

            self.change_x = -5  # makes the bird move left

            self.angle += self.change_angle  # change angle
            self.change_angle += self.ANGLE_AC  # how fast does angle accelerate
            if self.angle <= -45:  # adds limit to dipping down
                self.angle = -45  # stay on  angle
            if self.angle >= 55:  # adds limit to dipping upd
                self.angle = 55  # stay on 45 angle

        elif self.dir == "right":  # things that happen when bird is going right
            self.textures = self.texture_list  # choose frames that are turned right

            self.change_x = 5  # makes the bird move right

            self.angle += self.change_angle  # change angle
            self.change_angle -= self.ANGLE_AC  # how fast does angle accelerate
            if self.angle <= -55:  # adds limit to dipping down
                self.angle = -55  # stay on -45 angle
            if self.angle >= 45:  # adds limit to dipping up
                self.angle = 45  # stay on 55 angle

    def angle_control(self):  # controlling angle change to prevent bugs
        if self.dir == "right":  # setting for going right
            # sets limit for change angel
            if self.change_angle <= -5:
                self.change_angle = -5
            if self.change_angle >= 5:
                self.change_angle = 5

        if self.dir == "left":  # setting for going left
            # sets limit for change angel
            if self.change_angle <= -5:
                self.change_angle = -5
            if self.change_angle >= 5:
                self.change_angle = 5

        if self.center_y <= 50:
            self.angle = 0


# Coin class, sprites from /coin
class Coin(Animate):
    def __init__(self):
        super().__init__("../coin/coin-1.png", 2.5)
        self.random_pos()
        """Frames"""  # appending all off the frames to coin textures
        self.append_texture(arcade.load_texture("../coin/coin-2.png"))
        self.append_texture(arcade.load_texture("../coin/coin-3.png"))
        self.append_texture(arcade.load_texture("../coin/coin-4.png"))
        self.append_texture(arcade.load_texture("../coin/coin-5.png"))
        self.append_texture(arcade.load_texture("../coin/coin-6.png"))
        self.append_texture(arcade.load_texture("../coin/coin-5.png"))
        self.append_texture(arcade.load_texture("../coin/coin-4.png"))
        self.append_texture(arcade.load_texture("../coin/coin-3.png"))
        self.append_texture(arcade.load_texture("../coin/coin-2.png"))

    def setup(self):
        self.center_y = SCREEN_HEIGHT / 2
        self.center_x = SCREEN_WIDTH / 2

    def random_pos(self):
        """Start position"""
        self.center_x = random.randint(100, 700)  # starts with random pos on x
        self.center_y = random.randint(70, 530)  # starts with random pos on y


# Spike class, spawns mechanics, sprites from /DodgeBird
class Spike(arcade.Sprite):
    def __init__(self):
        super().__init__("../spike2.png", 1.7)
        self.type = random.randint(0, 2)  # gives random type to the spike
        if self.type == 0:  # type 0 makes it spawn from above
            self.center_x = random.randint(30, 770)
            self.center_y = SCREEN_HEIGHT
            self.change_y = -SPIKE_SPEED
            self.change_x = 0
            self.angle = 270
        if self.type == 1:  # type 1 makes spawn from left border
            self.center_x = 0
            self.center_y = random.randint(50, 550)
            self.change_y = 0
            self.change_x = SPIKE_SPEED
        if self.type == 2:  # type 2 makes spawn from right border
            self.center_x = SCREEN_WIDTH
            self.center_y = random.randint(50, 550)
            self.change_y = 0
            self.change_x = -SPIKE_SPEED
            self.angle = 180

    def update(self):
        self.center_y += self.change_y  # movement code
        self.center_x += self.change_x
        """Collision with screen borders"""  # The spike gets deleted, so no lag happens
        if self.center_y < 0:
            self.kill()
        if self.center_y > SCREEN_HEIGHT:
            self.kill()
        if self.center_x < 0:
            self.kill()
        if self.center_x > SCREEN_WIDTH:
            self.kill()


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.setup()  # turns on when game starts
        self.load_fonts()

    def load_fonts(self):
        self.pixel_custom_font = arcade.load_font("../VT323-Regular.ttf")

    def setup(self):
        self.run = True  # Starts the game
        """Bg:s"""
        self.bg = arcade.load_texture("../backorund.png")  # loading different bg:s
        self.go = arcade.load_texture("../GameOver.png")

        """Sprites"""  # initilizing the sprites
        self.bird = Bird()
        self.coin = Coin()
        self.coin.setup()

        """Sprite Lists"""
        self.spikes = arcade.SpriteList()  # list for spikes

        """"Sound"""  # sound uses from /sound
        self.jump_sound = arcade.load_sound("../sound/jump.wav")  # sound for jump
        self.explosion = arcade.load_sound("../sound/explosion.wav")  # sound for game over
        self.coin_sound_list = [arcade.load_sound("../sound/pickupCoin.wav"),  # makes list with three different sounds
                                arcade.load_sound("../sound/pickupCoin_1.wav"),
                                arcade.load_sound("../sound/pickupCoin_2.wav")]
        self.hit_sound_list = [arcade.load_sound("../sound/hitHurt1.wav"),
                               arcade.load_sound("../sound/hitHurt2.wav"),
                               arcade.load_sound("../sound/hitHurt3.wav")]

        """Fonts"""
        # self.pixel_custom_font = arcade.load_font("VT323-Regular.ttf")

        """"Other"""
        self.fps = 0  # fps counter starts with 0
        self.fps_limit = 60  # cd for spikes to spawn
        self.score = 0  # start score is 0

    # when run is not True, sprite do not render
    def on_draw(self):
        if self.run:
            self.clear()
            """Bg"""
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,  # function for loading the background
                                          SCREEN_HEIGHT / 2, SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.bg)

            """Sprites"""  # draws all the sprites
            self.bird.draw()
            self.coin.draw()
            self.spikes.draw()
            """Text"""
            arcade.draw_text(f"{self.score}",  # function for drawing text
                             10, 10,
                             font_size=20,
                             font_name=self.pixel_custom_font)
        else:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,  # if game is off load game over bg
                                          SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.go)
            arcade.draw_text(f"{self.score}! Press E",  # load text with the score in the middle of the screen
                             280, 300,
                             arcade.color.GOLD,
                             60,
                             100,
                             "left",
                             font_name=self.pixel_custom_font)

    def on_update(self, delta_time: float):  # things that happen every frame
        if self.run:
            """Sprites"""
            # __COIN__
            self.bird.update()
            self.bird.update_animation(delta_time)
            # __SPIKE__
            self.spikes.update()
            self.spawn_spike()
            # __COIN__
            self.coin.update()
            self.coin.update_animation(delta_time)

            """Game Collisions"""
            # __COIN n BIRD__
            if arcade.check_for_collision(self.coin, self.bird):  # Collisions with bird and coin
                self.score += 1  # add score when collide

                self.coin.random_pos()  # the coin is teleporting to random pos
                arcade.play_sound((random.choice(self.coin_sound_list)))  # play the random coin sound from \sound

                if self.score < 70:  # do not increase the spawn rate if player hit 70 score
                    self.fps_limit -= self.score * 0.02  # decrease spawn time for spikes
            # __BIRD n SPIKES__
            if arcade.check_for_collision_with_list(self.bird, self.spikes):  # if player touches spike
                arcade.play_sound(self.explosion)  # play explosion sound from \sound
                self.run = False

    #  movement for player that uses w,a,s,d,space ds
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE or symbol == arcade.key.W or symbol == arcade.key.UP:  # if key SPACE, W, UP
            self.bird.jump()  # makes the bird jump

        if symbol == arcade.key.A:  # if key is A
            self.bird.dir = "left"
            self.bird.angle *= -1  # invert the angle of the bird

        if symbol == arcade.key.D:  # if key is D
            self.bird.dir = "right"

            self.bird.angle *= -1  # invert the angle of the bird

        # if the game is of
        if symbol == arcade.key.E:  # if key is E
            if not self.run:
                self.setup()  # restart the game

    def spawn_spike(self):
        self.fps += 1
        if self.fps >= self.fps_limit:
            self.fps = 0

        if self.score >= 1 and self.fps == 0:  # Spike spawn system
            self.spike = Spike()
            self.spikes.append(self.spike)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

print(window.bird.texture)

arcade.run()
