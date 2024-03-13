import arcade


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

coin_textures = coin.texture_list
bird_textures = bird.texture_list
bird_flipped_textures = bird.texture_flipped_list
