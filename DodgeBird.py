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
        super().__init__("bird/CUstombird-downflap.png", 2.5)  # giving start picture and scale
        # making list for frames
        self.texture_list = [(arcade.load_texture("bird/CUstombird-downflap.png")),
                             (arcade.load_texture("bird/Custombird-midflap.png")),
                             (arcade.load_texture("bird/Custombird-upflap.png"))
                             ]
        # making another list for flipped frames
        self.texture_flipped_list = [(arcade.load_texture("bird/CUstombird-downflap.png", flipped_horizontally=True)),
                                     (arcade.load_texture("bird/Custombird-midflap.png", flipped_horizontally=True)),
                                     (arcade.load_texture("bird/Custombird-upflap.png", flipped_horizontally=True))
                                     ]

        """Start position"""
        self.center_x = 100  # start position on x
        self.center_y = SCREEN_WIDTH / 2  # start position on y
        self.change_y = 0  # start without force

    def update(self):
        """gravity"""
        self.center_y += self.change_y  # code for gravity
        self.change_y -= GRAVITATION

        """Collision with screen borders"""  # makes bird stop when touching border
        if self.center_y <= 20:
            self.center_y = 20
        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        if self.center_x <= 0:
            self.center_x = 0
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH

        """Horizontally movement"""
        self.center_x += self.change_x  # This makes the sprite move

    def turn(self, flip):  # function to change between flipped frames and not
        if flip:
            self.textures = self.texture_list
        else:
            self.textures = self.texture_flipped_list

    # Coin class, sprites from /coin


class Coin(Animate):
    def __init__(self):
        super().__init__("coin/coin-1.png", 2.5)
        """Frames"""  # appending all off the frames to coin textures
        self.append_texture(arcade.load_texture("coin/coin-2.png"))
        self.append_texture(arcade.load_texture("coin/coin-3.png"))
        self.append_texture(arcade.load_texture("coin/coin-4.png"))
        self.append_texture(arcade.load_texture("coin/coin-5.png"))
        self.append_texture(arcade.load_texture("coin/coin-6.png"))
        self.append_texture(arcade.load_texture("coin/coin-5.png"))
        self.append_texture(arcade.load_texture("coin/coin-4.png"))
        self.append_texture(arcade.load_texture("coin/coin-3.png"))
        self.append_texture(arcade.load_texture("coin/coin-2.png"))

        self.center_x = random.randint(100, 700)  # starts with random pos on x
        self.center_y = random.randint(70, 530)  # starts with random pos on x


# Spike class, spawns mechanics, sprites from /DodgeBird
class Spike(arcade.Sprite):
    def __init__(self):
        super().__init__("spike2.png", 1.7)
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

    def setup(self):
        self.run = True  # Starts the game
        """Bg:s"""
        self.bg = arcade.load_texture("backorund.png")  # loading different
        self.go = arcade.load_texture("GameOver.png")

        """Sprites"""  # initilizing the sprites
        self.bird = Bird()
        self.coin = Coin()

        """Sprite Lists"""
        self.spikes = arcade.SpriteList()  # list for spikes

        """"Other"""
        self.fps = 0  # fps counter starts with 0
        self.fps_limit = 60  # cd for spikes to spawn
        self.score = 0  # start score is 0

        """"Sound"""  # sound uses from /sound
        self.coin_sound_list = [arcade.load_sound("sound/pickupCoin.wav"),  # makes list with three different sounds
                                arcade.load_sound("sound/pickupCoin_1.wav"),
                                arcade.load_sound("sound/pickupCoin_2.wav")]
        self.jump_sound = arcade.load_sound("sound/jump.wav")  # sound for jump
        self.explosion = arcade.load_sound("sound/explosion.wav")  # sound for game over

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
                             20, 550,
                             arcade.color.GOLD, 30)
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
                             "left")

    def on_update(self, delta_time: float):
        if self.run:
            """Sprites"""
            self.bird.update()
            self.bird.update_animation(delta_time)

            self.spikes.update()

            self.coin.update()
            self.coin.update_animation(delta_time)

            """Spikes spawner"""
            self.fps += 1
            if self.fps >= self.fps_limit:
                self.fps = 0

            if self.score >= 1 and self.fps == 0:  # Spike spawn system
                self.spike = Spike()
                self.spikes.append(self.spike)

            """Game Collisions"""
            if arcade.check_for_collision(self.coin, self.bird):  # Collisions with bird and coin
                self.score += 1  # add score when collide
                self.coin.center_x = random.randint(100, 700)  # random position
                self.coin.center_y = random.randint(70, 530)
                self.fps_limit -= self.score * 0.02  # decrease spawn time for spikes
                arcade.play_sound((random.choice(self.coin_sound_list)))

            if arcade.check_for_collision_with_list(self.bird, self.spikes):
                arcade.play_sound(self.explosion)
                self.run = False

    #  movement for player that uses w,a,s,d,space
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.bird.change_y = BIRD_SPEED
            arcade.play_sound(self.jump_sound)

        if symbol == arcade.key.A:
            self.bird.change_x = -5
            self.bird.turn(False)
        if symbol == arcade.key.D:
            self.bird.change_x = 5
            self.bird.turn(True)

        # if the game is of
        if symbol == arcade.key.E:
            if not self.run:
                self.setup()


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

print(window.bird.texture)

arcade.run()
