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

    def update_animation(self, delta_time):  # swaps between textures based on delta_time
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
        super().__init__("bird/CUstombird-downflap.png", 2.5)
        self.append_texture(arcade.load_texture("bird/Custombird-midflap.png"))
        self.append_texture(arcade.load_texture("bird/Custombird-upflap.png"))

        self.center_x = 100
        self.center_y = SCREEN_WIDTH / 2  # start position

        self.change_y = 0  # start without force

    def update(self):
        """gravity"""
        self.center_y += self.change_y  # code for gravity
        self.change_y -= GRAVITATION

        """Collision with screen borders"""
        if self.center_y <= 40:
            self.center_y = 40
        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        if self.center_x <= 0:
            self.center_x = 0
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH

        """Horizontally movement"""
        self.center_x += self.change_x


class Coin(Animate):
    def __init__(self):
        super().__init__("coin/coin-1.png", 2.5)
        """Frames"""
        self.append_texture(arcade.load_texture("coin/coin-2.png"))
        self.append_texture(arcade.load_texture("coin/coin-3.png"))
        self.append_texture(arcade.load_texture("coin/coin-4.png"))
        self.append_texture(arcade.load_texture("coin/coin-5.png"))
        self.append_texture(arcade.load_texture("coin/coin-6.png"))
        self.append_texture(arcade.load_texture("coin/coin-5.png"))
        self.append_texture(arcade.load_texture("coin/coin-4.png"))
        self.append_texture(arcade.load_texture("coin/coin-3.png"))
        self.append_texture(arcade.load_texture("coin/coin-2.png"))

        self.center_x = random.randint(100, 700)  # starts with random pos
        self.center_y = random.randint(70, 530)


class Spike(arcade.Sprite):
    def __init__(self):
        super().__init__("spike2.png", 1.7)
        self.type = random.randint(0, 2)
        if self.type == 0:  # different spawn point for spike
            self.center_x = random.randint(30, 770)
            self.center_y = SCREEN_HEIGHT
            self.change_y = -SPIKE_SPEED
            self.change_x = 0
            self.angle = 90
        if self.type == 1:
            self.center_x = 0
            self.center_y = random.randint(50, 550)
            self.change_y = 0
            self.change_x = SPIKE_SPEED
        if self.type == 2:
            self.center_x = SCREEN_WIDTH
            self.center_y = random.randint(50, 550)
            self.change_y = 0
            self.change_x = -SPIKE_SPEED
            self.angle = 180

    def update(self):
        self.center_y += self.change_y  # movement code
        self.center_x += self.change_x

        """Collision with screen borders"""
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
        self.setup()
        self.run = True  # Starts the game
        """Bg:s"""
        self.bg = arcade.load_texture("backorund.png")  # loading different
        self.go = arcade.load_texture("GameOver.png")

        """Sprites"""
        self.bird = Bird()
        self.coin = Coin()

        """Sprite Lists"""
        self.spikes = arcade.SpriteList()  # list for spikes

        """"Other"""
        self.fps = 0  # fps counter starts with 0
        self.fps_limit = 60  # cd for spikes to spawn
        self.score = 0  # start score is 0

        self.pixel_font = arcade.load_font("dogicapixel.otf")

        """"Sound"""
        self.coin_sound_list = [arcade.load_sound("sound/pickupCoin.wav"),
                                arcade.load_sound("sound/pickupCoin_1.wav"),
                                arcade.load_sound("sound/pickupCoin_2.wav")]
        self.jump_sound = arcade.load_sound("sound/jump.wav")
        self.explosion = arcade.load_sound("sound/explosion.wav")

    def setup(self):
        self.run = True  # Starts the game
        self.fps = 0  # fps counter starts with 0
        self.fps_limit = 60  # cd for spikes to spawn
        self.score = 0  # start score is 0


    def on_draw(self):
        if self.run:
            self.clear()
            """Bg"""
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                          SCREEN_HEIGHT / 2, SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.bg)

            """Sprites"""
            self.bird.draw()
            self.coin.draw()
            self.spikes.draw()
            """Text"""
            arcade.draw_text(f"{self.score}",
                             20, 550,
                             arcade.color.GOLD, 30)
        else:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                          SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH,  # if game is off load game over bg
                                          SCREEN_HEIGHT, self.go)
            arcade.draw_text(f"{self.score}! Press E",  # load text with the score in the middle of the screen
                             280, 300,
                             arcade.color.GOLD,
                             60,
                             100,
                             "left",
                             font_name=arcade.load_font("dogicapixel.ttf"))

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

    def on_key_press(self, symbol: int, modifiers: int):  # movement for bird
        if symbol == arcade.key.SPACE:
            self.bird.change_y = BIRD_SPEED
            arcade.play_sound(self.jump_sound)
        if symbol == arcade.key.A:
            self.bird.change_x = -5
        if symbol == arcade.key.D:
            self.bird.change_x = 5
        if symbol == arcade.key.E:
            if not self.run:
                window.close()


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

print(window.bird.texture)

arcade.run()