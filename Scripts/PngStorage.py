import arcade


# Stores all the frames for coin
class Coin():
    def __init__(self):
        self.texture_list = [arcade.load_texture("../coin/coin-1.png"),
                             arcade.load_texture("../coin/coin-2.png"),
                             arcade.load_texture("../coin/coin-3.png"),
                             arcade.load_texture("../coin/coin-4.png"),
                             arcade.load_texture("../coin/coin-5.png"),
                             arcade.load_texture("../coin/coin-6.png"),
                             arcade.load_texture("../coin/coin-5.png"),
                             arcade.load_texture("../coin/coin-4.png"),
                             arcade.load_texture("../coin/coin-3.png"),
                             arcade.load_texture("../coin/coin-2.png")]


# Stores all the frames for bird
class Bird():
    def __init__(self):
        self.texture_list = [(arcade.load_texture("../Bird/CUstombird-downflap.png")),
                             (arcade.load_texture("../Bird/Custombird-midflap.png")),
                             (arcade.load_texture("../Bird/Custombird-upflap.png"))
                             ]

        self.texture_flipped_list = [
            (arcade.load_texture("../Bird/CUstombird-downflap.png", flipped_horizontally=True)),
            (arcade.load_texture("../Bird/Custombird-midflap.png", flipped_horizontally=True)),
            (arcade.load_texture("../Bird/Custombird-upflap.png", flipped_horizontally=True))
        ]


coin = Coin()
bird = Bird()

# Creating all the texture lists
coin_textures = coin.texture_list
bird_textures = bird.texture_list
bird_flipped_textures = bird.texture_flipped_list
