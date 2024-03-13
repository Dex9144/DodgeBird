import arcade
import random
import base64
import time
from PngStorage import coin_textures, bird_textures, bird_flipped_textures

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "DodgeBird"

BIRD_SPEED = 6  # how high the bird jump
GRAVITATION = 0.4  # gravitation force

SPIKE_SPEED = 5


# Animate class, uses for animate sprites
class Animate(arcade.Sprite):
    i = 0
    time = 0

    def update_animation(self, delta_time):  # Swaps between textures based on delta_time
        self.time += delta_time
        if self.time >= 0.1:
            self.time = 0
            if self.i == len(self.textures) - 1:
                self.i = 0
            else:
                self.i += 1
                self.set_texture(self.i)


# Bird class, player controlled object, sprites from /Bird
class Bird(Animate):
    def __init__(self):
        super().__init__("../Bird/CUstombird-downflap.png", 2.5)  # Giving start picture and scale
        """Textures"""
        # __List for normal and flipped frames__
        self.texture_list = bird_textures  # Taking the frames from the PngStorage.py
        self.texture_flipped_list = bird_flipped_textures  # Taking the frames from the PngStorage.py
        self.textures = self.texture_list  # Setting the start textures
        # __Animation delay__
        self.time = 10  # Time delay for the animation

        """Start position"""
        self.center_x = SCREEN_WIDTH / 2  # Start position on x
        self.center_y = 10  # Start position on y
        self.change_y = 0  # Start without force

        """Start dir, angle"""
        self.dir = ""  # Direction is right
        self.angle = 0  # Angle is 0
        self.change_angle = 0  # Angle force is 0
        self.ANGLE_AC = 0.5  # This is how fast the bird dips down

        """Other"""
        self.hit_sound_played = False  # Player is not hitting the ground when game starts

    def update(self):  # Things that happen every frame
        """gravity"""
        self.center_y += self.change_y
        self.change_y -= GRAVITATION

        """Collision with screen borders and ground"""  # Makes bird stop when touching border
        if self.center_y <= 45:  # "ground" is on y 45
            self.center_y = 45
            # Makes sound when hitting the ground
            if not self.hit_sound_played:  # If bird did not hit the ground
                arcade.play_sound((random.choice(window.hit_sound_list)))  # Play the sound from \sound
                self.hit_sound_played = True  # Bird did hit the ground
        # Make the hit sound possible after the bird leaving the ground
        if self.center_y != 45:
            self.hit_sound_played = False

        if self.center_y >= SCREEN_HEIGHT - 20:
            self.center_y = SCREEN_HEIGHT - 20
        if self.center_x <= 26:
            self.center_x = 26
        if self.center_x >= SCREEN_WIDTH - 26:
            self.center_x = SCREEN_WIDTH - 26

        """Horizontally movement"""
        self.center_x += self.change_x  # The x force is always adding to the x pos

        """Angle"""
        self.turn_sprite()  # Checking which way the bird is going
        self.angle_control()  # Control the change_angle
        print(self.center_y)  # DEBUG

    def jump(self):  # All things that happen when bird is jumping
        self.change_y = BIRD_SPEED  # Bird goes up
        arcade.play_sound(window.jump_sound)  # Plays the jump sound from \sound

        # The angle goes up based on what dir
        if self.dir == "right":
            self.change_angle += 50  # Dip up the bird
        if self.dir == "left":
            self.change_angle += -50  # Dip up the bird

    def turn_sprite(self):  # Turn function manages all thing when player is turning

        if self.dir == "left":  # Things that happen when bird is going left
            self.textures = self.texture_flipped_list  # Using frames that are turned left

            self.change_x = -5  # Makes the bird move left

            self.angle += self.change_angle  # Change angle
            self.change_angle += self.ANGLE_AC  # How fast does angle accelerate
            if self.angle <= -45:  # Adds limit to dipping down
                self.angle = -45  # Stay on  angle
            if self.angle >= 55:  # Adds limit to dipping upd
                self.angle = 55  # Stay on 45 angle

        elif self.dir == "right":  # Things that happen when bird is going right
            self.textures = self.texture_list  # Choose frames that are turned right

            self.change_x = 5  # Makes the bird move right

            self.angle += self.change_angle  # Change angle
            self.change_angle -= self.ANGLE_AC  # How fast does angle accelerate
            if self.angle <= -55:  # Adds limit to dipping down
                self.angle = -55  # Stay on -45 angle
            if self.angle >= 45:  # Adds limit to dipping up
                self.angle = 45  # Stay on 55 angle

    def angle_control(self):  # Controlling angle change to prevent bugs
        if self.dir == "right":  # Setting for going right
            # Sets limit for change angel
            if self.change_angle <= -5:
                self.change_angle = -5
            if self.change_angle >= 5:
                self.change_angle = 5

        if self.dir == "left":  # Setting for going left
            # Sets limit for change angel
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
        self.setup()  # run the setup function

        self.textures = coin_textures  # Taking all the frames from PngStorage

        self.start_center_y = self.center_y  # Taking the start pos
        self.change_y = 0.4  # Speed of the bouncing

    # __Start settings for coin__
    def setup(self):
        self.center_y = SCREEN_HEIGHT / 2
        self.center_x = SCREEN_WIDTH / 2

    # __Makes coin go up and down__
    def bounce(self):
        if self.center_y >= self.start_center_y + 6:
            self.change_y *= -1
        if self.center_y <= self.start_center_y - 6:
            self.change_y *= -1

    # __Function that happens every frame__
    def update(self):
        self.bounce()
        self.center_y += self.change_y

    # __Function that gives random pos__
    def random_pos(self):
        """Start position"""
        self.center_x = random.randint(100, 700)  # starts with random pos on x
        self.center_y = random.randint(70, 530)  # starts with random pos on y

        self.start_center_y = self.center_y


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

# The main Game class
class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.setup()  # Turn on the start settings when game starts
        self.load_fonts()  # __!WORKING ON!__

        self.high_score = self.read_high_score()  # Loading the high score from \Scripts\Info

    # __!WORKING ON!__
    def load_fonts(self):
        self.pixel_custom_font = arcade.load_font("../VT323-Regular.ttf")

    # __Function to read the saved high score
    def read_high_score(self):
        try:
            with open("Info", 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0  # If the file doesn't exist, return 0 as the high score
        return self.high_score
        # __!CHEAT = NO BITCHES!__

    # __Function to save the high score__
    def write_high_score(self):
        with open("Info", "w") as file:
            file.write(str(self.high_score))
        # __!CHEAT = NO BITCHES!__

    # __Function that runs at the start__
    def setup(self):
        self.run = True  # Starts the game
        """Bg:s"""
        self.bg = arcade.load_texture("../backorund.png")  # Loading bg
        self.go = arcade.load_texture("../GameOver.png")  # Loading GameOver bg

        """Sprites"""
        self.bird = Bird()  # Spawning Bird
        self.coin = Coin()  # Spawning Coin

        """Sprite Lists"""
        self.spikes = arcade.SpriteList()  # Creating enemy list for spikes

        """"Sound"""  # Sound uses from /sound
        self.jump_sound = arcade.load_sound("../sound/jump.wav")  # Sound for jump
        self.explosion = arcade.load_sound("../sound/explosion.wav")  # Sound for lose
        self.coin_sound_list = [arcade.load_sound("../sound/pickupCoin.wav"),  # List with different pick up coin sounds
                                arcade.load_sound("../sound/pickupCoin_1.wav"),
                                arcade.load_sound("../sound/pickupCoin_2.wav")]
        self.hit_sound_list = [arcade.load_sound("../sound/hitHurt1.wav"),  # List with different hit sounds
                               arcade.load_sound("../sound/hitHurt2.wav"),
                               arcade.load_sound("../sound/hitHurt3.wav")]

        """Fonts"""  # Not in work
        # self.pixel_custom_font = arcade.load_font("VT323-Regular.ttf")

        """"Other"""
        self.fps = 0  # Fps counter starts with 0
        self.fps_limit = 60  # Cd for spikes to spawn
        self.score = 0  # Start score is 0

    # __Draws object on screen, happens every frame__
    def on_draw(self):
        if self.run:  # If game runs
            self.clear()  # Clearing screen every frame to prevent overlaying
            """Bg"""
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,  # Function for draw the background
                                          SCREEN_HEIGHT / 2, SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.bg)

            """Sprites"""  # Draw all the sprites
            self.bird.draw()
            self.coin.draw()
            self.spikes.draw()

        self.text()  # Draw the texts

    # __Function that runs every frame__
    def on_update(self, delta_time: float):  # Things that happen every frame
        if self.run:  # If game runs
            """Sprites"""
            # __COIN__
            self.bird.update()  # Update bird, bird animation
            self.bird.update_animation(delta_time)
            # __SPIKE__
            self.spikes.update()  # Update all the spikes, spikes functions
            self.spawn_spike()
            # __COIN__
            self.coin.update()  # Update coin, coin animation
            self.coin.update_animation(delta_time)

            """Game Collisions"""
            # __COIN n BIRD__
            if arcade.check_for_collision(self.coin, self.bird):  # Collisions with bird and coin
                self.score += 1  # Add score when collide

                self.coin.random_pos()  # The coin is teleporting to random pos
                arcade.play_sound((random.choice(self.coin_sound_list)))  # Play the random coin sound from \sound

                if self.score < 70:  # Do not increase the spawn rate of spikes if player hit 70 score
                    self.fps_limit -= self.score * 0.02  # Decrease spawn time for spikes
            # __BIRD n SPIKES__
            if arcade.check_for_collision_with_list(self.bird, self.spikes):  # If player touches spike
                arcade.play_sound(self.explosion)  # Play explosion sound from \sound
                self.run = False  # Shut the game

        """Check high score"""
        if self.score > self.high_score:  # Set new high score if score is more than high score
            self.high_score = self.score
        if not self.run:  # If you lost write the highscore
            self.write_high_score()  # Write down the high score in txt

    #  __Function for input__
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE or symbol == arcade.key.W or symbol == arcade.key.UP:  # if key SPACE, W, UP
            self.bird.jump()  # makes the bird jump

        if symbol == arcade.key.A:  # If key is A
            self.bird.dir = "left"  # Makes the bird move left
            self.bird.angle *= -1  # Invert the angle of the bird

        if symbol == arcade.key.D:  # If key is D
            self.bird.dir = "right"  # Makes the bird move right
            self.bird.angle *= -1  # Invert the angle of the bird

        if symbol == arcade.key.E:  # if key you lose and press E, the game restarts
            if not self.run:
                self.setup()

                # __Function for spawning spikes__

    def spawn_spike(self):
        self.fps += 1  # My clock for spikes, because why not
        if self.fps >= self.fps_limit:
            self.fps = 0

        if self.score >= 1 and self.fps == 0:  # Spawn spike when clock resets
            self.spike = Spike()
            self.spikes.append(self.spike)  # Append the sprite to the enemy list

    # __All the text in game__
    def text(self):
        if self.run:  # This text is drawn if game is running
            # __Score in game__
            arcade.draw_text(f"{self.score}",  # function for drawing text
                             10, 10,
                             font_size=20,
                             font_name=self.pixel_custom_font)

        else:  # These texts are drawn if game is shut, I know that background picture is not a text
            # __GO bg__
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2,
                                          SCREEN_HEIGHT / 2,
                                          SCREEN_WIDTH,
                                          SCREEN_HEIGHT, self.go)
            # __Score in GO__
            arcade.draw_text(f"{self.score}!",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.GOLD,
                             60,
                             100,
                             "left",
                             font_name=self.pixel_custom_font)
            # __Press E to restart__
            arcade.draw_text("Press E to restart",
                             (SCREEN_WIDTH / 2) - 20, (SCREEN_HEIGHT / 2) - 30,
                             arcade.color.GOLD,
                             10,
                             100,
                             "left",
                             font_name=self.pixel_custom_font)
            # __Show the best score__
            arcade.draw_text(f"Best: {self.high_score}",
                             (SCREEN_WIDTH / 2) + 10, (SCREEN_HEIGHT / 2) + 70,
                             arcade.color.GOLD,
                             10,
                             100,
                             "left",
                             font_name=self.pixel_custom_font)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

arcade.run()
